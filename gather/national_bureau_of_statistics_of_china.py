import re
import time

import requests

from util.config import get_config


def _send_request(url, method, body=None):
    """
    发送请求
    :param url: url地址
    :param method: 请求方式
    :param body: body数据
    :return: 请求结果
    """
    # 请求发起时 是否暂停
    # time.sleep(int(get_config("gather", "sleepTime")))
    time.sleep(5)
    headers = {'Content-Type': "text/html;charset=GB2312",
               'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    if method == "get":
        response = requests.get(url, headers=headers)
        response.encoding = "GBK"
    else:
        response = requests.post(url, headers=headers, body=body)
    response_text = response.text
    response.close()
    return response_text


def get_city_data_list(url, postfix):
    """
    获取市数据列表
    :param url: 地址
    :param postfix: 后缀
    :return: 市列表
    """
    url = url + postfix +".html"
    response = _send_request(url, "get")
    # print(response)
    pattern = re.compile("<tr class='citytr'><td><a href='.*?'>(.*?)</a></td><td><a href='(.*?).html'>(.*?)</a></td></tr>")
    areas = re.findall(pattern, response)
    return areas


def get_province_data_list(url):
    """
    获取省数据列表
    :param url: 地址
    :return: 省列表
    """
    response = _send_request(url, "get")
    # print(response)
    pattern = re.compile("<a href='(.*?).html'>(.*?)<br/></a>")
    areas = re.findall(pattern, response)
    return areas

def start():
    print("开始采集中国统计局数据->数据补全")
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"
    for province_data in get_province_data_list(url):
        for city_data in get_city_data_list(url,province_data[0]):
            for county_data in get_city_data_list(url,city_data[1]):
                print(county_data)
        # for

if __name__ == '__main__':

    start()
    # print(get_city_data_list(url, "11.html"))
