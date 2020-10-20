"""中国民政部"""
import time

import re
from urllib.parse import quote

import requests

from dao import administrative_division_dao, administrative_level_dao, administrative_type_dao
from gather.gather_exception import GatherException
from model.administrative_division import AdministrativeDivision
from util.config import get_config


def send_request(url, method, body=None):
    """
    发送请求
    :param url: url地址
    :param method: 请求方式
    :param body: body数据
    :return: 请求结果
    """
    # 请求发起时 是否暂停
    time.sleep(int(get_config("gather", "sleepTime")))
    headers = {'Content-Type': "text/html;charset=GBK",
               'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    if method == "get":
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, body=body)
    response_text = response.text
    response.close()
    return response_text


def _regular_values(response):
    """
    正则取值
    :param response: 返回结果
    :return: 正则取值结果
    """
    pattern = re.compile(
        r'\{"children":\[],"diji":"(.*?)","quHuaDaiMa":"(.*?)","quhao":"(.*?)","shengji":"(.*?)","xianji":"(.*?)"}')
    areas = re.findall(pattern, response)
    return areas


def get_province_data_list():
    """
    获取省数据列表
    :return: 结果
    """
    url = "http://xzqh.mca.gov.cn/map"
    # 发送请求
    response = send_request(url, "get")
    # 封装并直接返回结果
    return _regular_values(response)


def get_province(province_data, parent_administrative_division_id):
    """
    获取省行政区划
    :param province_data: 省数据
    :param parent_administrative_division_id: 上级id
    :return:
    """
    province_name = re.sub("\(.*?\)", "", province_data[3])
    # 获取省名称后缀
    administrativeDivision = administrative_division_dao.find_administrative_division_by_name(province_name)
    # TODO 可以验证数据是否正确
    if administrativeDivision is None:
        administrativeDivision = AdministrativeDivision(0, province_name, 0, 0, province_data[1][0:2], 0)
        administrative_level_name = administrativeDivision.name[len(administrativeDivision.name) - 1]
        # 判断是否为省
        if administrative_level_name == "省":
            administrative_level_id = administrative_level_dao.save_or_find_level_by_name("省").id
            administrative_type_id = administrative_type_dao.save_or_find_type_by_name("省级").id
        elif administrative_level_name == "市":
            administrative_level_id = administrative_level_dao.save_or_find_level_by_name("市").id
            administrative_type_id = administrative_type_dao.save_or_find_type_by_name("省级").id
        else:
            # 重新获取一次省名称后缀
            administrative_level_name = administrativeDivision.name[
                                        len(administrativeDivision.name) - 3:len(administrativeDivision.name)]
            if administrative_level_name == "自治区":
                administrative_level_id = administrative_level_dao.save_or_find_level_by_name("自治区").id
                administrative_type_id = administrative_type_dao.save_or_find_type_by_name("省级").id
            else:
                # 再次获取省名称后缀
                administrative_level_name = administrativeDivision.name[
                                            len(administrativeDivision.name) - 5:len(administrativeDivision.name)]
                if administrative_level_name == "特别行政区":
                    administrative_level_id = administrative_level_dao.save_or_find_level_by_name("特区").id
                    administrative_type_id = administrative_type_dao.save_or_find_type_by_name("特别行政区").id
                else:
                    raise GatherException(province_name + "名称异常！请联系开发人员修改数据")
        administrativeDivision.administrative_level_id = administrative_level_id
        administrativeDivision.administrative_type_id = administrative_type_id
        administrativeDivision.parent_administrative_division_id = parent_administrative_division_id
        administrativeDivision = administrative_division_dao.save(administrativeDivision)
    return administrativeDivision


def get_city_and_county_data_list(province_data_name, city_data_name=None, county_data_name=None):
    """
    获取市或者县数据列表
    :param province_data_name: 省名称
    :param city_data_name: 市名称
    :param county_data_name: 县名称
    :return: 市和县数据列表
    """
    province = quote(province_data_name, encoding="GB2312")
    if city_data_name is None:
        url = "http://xzqh.mca.gov.cn/advancedDataQueryDefaut?shengji=" + province + "&diji=-1&xianji=-1&tp=-1&leiXing=-1&fangfa1=&shuliang1=&fangfa2=&shuliang2=&fangfa3=&shuliang3=&fangfa4=&shuliang4=&fangfa5=&shuliang5=&fangfa6=&shuliang6=&fangfa7=&shuliang7=&fangfa8=&shuliang8=&fangfa9=&shuliang9=&fangfa10=&shuliang10=&fangfa11=&shuliang11=&fangfa12=&shuliang12=&fangfa13=&shuliang13=&fangfa14=&shuliang14=&fangfa15=&shuliang15=&fangfa16=&shuliang16=&fangfa17=&shuliang17=&fangfa18=&shuliang18=&fangfa19=&shuliang19="
    elif county_data_name is None:
        city = quote(city_data_name, encoding="GB2312")
        url = "http://xzqh.mca.gov.cn/advancedDataQueryDefaut?shengji=" + province + "&diji=" + city + "&xianji=-1&tp=-1&leiXing=-1&fangfa1=&shuliang1=&fangfa2=&shuliang2=&fangfa3=&shuliang3=&fangfa4=&shuliang4=&fangfa5=&shuliang5=&fangfa6=&shuliang6=&fangfa7=&shuliang7=&fangfa8=&shuliang8=&fangfa9=&shuliang9=&fangfa10=&shuliang10=&fangfa11=&shuliang11=&fangfa12=&shuliang12=&fangfa13=&shuliang13=&fangfa14=&shuliang14=&fangfa15=&shuliang15=&fangfa16=&shuliang16=&fangfa17=&shuliang17=&fangfa18=&shuliang18=&fangfa19=&shuliang19="
    else:
        city = quote(city_data_name, encoding="GB2312")
        county = quote(county_data_name, encoding="GB2312")
        url = "http://xzqh.mca.gov.cn/advancedDataQueryDefaut?shengji=" + province + "&diji=" + city + "&xianji=" + county + "&tp=-1&leiXing=-1&fangfa1=&shuliang1=&fangfa2=&shuliang2=&fangfa3=&shuliang3=&fangfa4=&shuliang4=&fangfa5=&shuliang5=&fangfa6=&shuliang6=&fangfa7=&shuliang7=&fangfa8=&shuliang8=&fangfa9=&shuliang9=&fangfa10=&shuliang10=&fangfa11=&shuliang11=&fangfa12=&shuliang12=&fangfa13=&shuliang13=&fangfa14=&shuliang14=&fangfa15=&shuliang15=&fangfa16=&shuliang16=&fangfa17=&shuliang17=&fangfa18=&shuliang18=&fangfa19=&shuliang19="
    response = send_request(url,"get")
    response = response.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
    if response == '':
        return None
    pattern = re.compile(
        r'<tdflag="t1"name="shengJi"><.*?>(.*?)</a></td>'
        r'<tdflag="t2"name="diJi"><.*?>(.*?)</a></td>'
        r'<tdflag="t3"name="xianJi"><.*?>(.*?)</a></td>'
        # r'<tdflag="t4"name="zhuDi">(.*?)</td>'
        r'<tdflag=".*?t5"name="xingZhengJiBie">(.*?)</td>'
        r'<tdflag="t6"name="leiXing1">(.*?)</td>'
        r'<tdflag=".*?t13"name="quHuaDaiMa1".*?>(.*?)</td>')
    areas = re.findall(pattern, response)
    return areas


def get_city_or_county(city_and_county_data, parent_administrative_division_id):
    """
    获取市和县行政区划
    :param city_and_county_data: 市和县数据
    :param parent_administrative_division_id: 父级id
    :return: 市和县行政区划
    """
    # 如果下标位移2位标识县的id为空则该数据为市 否则为县
    if city_and_county_data[2] == '':
        city_or_county_data_name = city_and_county_data[1]
        city_or_county_data_code = str(city_and_county_data[5])[2:4]
    else:
        city_or_county_data_name = city_and_county_data[2]
        city_or_county_data_code = str(city_and_county_data[5])[4:6]

    if city_and_county_data[3] == '':
        administrative_level_id = None
    else:
        administrative_level_id = administrative_level_dao.save_or_find_level_by_name(city_and_county_data[3]).id
    if city_and_county_data[4] == '':
        administrative_type_id = None
    else:
        administrative_type_id = administrative_type_dao.save_or_find_type_by_name(city_and_county_data[4]).id
    # TODO 可以验证数据是否正确
    administrativeDivision = administrative_division_dao.find_administrative_division_by_name(city_or_county_data_name)
    if administrativeDivision is None:
        administrative_division = AdministrativeDivision(0, city_or_county_data_name, administrative_level_id,administrative_type_id, city_or_county_data_code,parent_administrative_division_id)
        administrativeDivision = administrative_division_dao.save(administrative_division)
    return administrativeDivision


def get_city_or_county_data_list(province_name,city_name = None):
    """获取市数据"""
    url = "http://xzqh.mca.gov.cn/selectJson"
    if city_name is None:
        body = ("shengji=" + province_name).encode('UTF-8')
    else:
        body = ("shengji=" + province_name + "&diji=" + city_name).encode('UTF-8')
    # body = "shengji='江苏省(苏)'"..encode('UTF-8')
    headers = {'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
               'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    response = str(requests.post(url, data=body, headers=headers).content, 'utf-8')
    return _regular_values(response)


def start(parent_administrative_division_id):
    """
    开始采集
    :param parent_administrative_division_id:
    :return:
    """
    print("开始采集中国民政部数据")
    for province_data in get_province_data_list():
        # 获取省名称
        province_data_name = province_data[3]
        # 封装administrativeDivision对象
        province = get_province(province_data, parent_administrative_division_id)
        province_division_id = province.id
        print("正在采集："+province_data_name)
        city_and_county_data_list = get_city_and_county_data_list(province_data_name)
        if city_and_county_data_list is not None:
            division_id = 0
            for city_and_county_data in city_and_county_data_list:
                # 如果市和县都为空则跳过该数据 专为台湾设立
                if city_and_county_data[2] == '' and city_and_county_data[1] == '':
                    continue
                # 如果下标位移2位标识县的id为空则该数据为市 否则为县
                if city_and_county_data[2] == '':
                    division_id = get_city_or_county(city_and_county_data, province_division_id).id
                else:
                    get_city_or_county(city_and_county_data, division_id)
        else:
            # 无法获取数据时则获取到市
            for city in get_city_or_county_data_list(province_data_name):
                city_data_name = city[0]
                city_data_list = get_city_and_county_data_list(province_data_name, city_data_name)
                if city_data_list is not None:
                    division_id = 0
                    for city_data in city_data_list:
                        # 如果市和县都为空则跳过该数据 专为台湾设立
                        if city_data[2] == '' and city_data[1] == '':
                            continue
                        # 如果下标位移2位标识县的id为空则该数据为市 否则为县
                        if city_data[2] == '':
                            division_id = get_city_or_county(city_data, province_division_id).id
                        else:
                            get_city_or_county(city_data, division_id)
                else:
                    for county in get_city_or_county_data_list(province_data_name, city_data_name):
                        county_data_name = county[4]
                        county_data_list = get_city_and_county_data_list(province_data_name, city_data_name,
                                                                         county_data_name)
                        if county_data_list is not None:
                            for county_data in county_data_list:
                                get_city_or_county(county_data, province_division_id)
                        else:
                            print(county)