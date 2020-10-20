from db.sqllie3.sqllite3_db import SQLlite3DB
from model.administrative_level import AdministrativeLevel


def find_administrative_level_by_id(id) -> AdministrativeLevel:
    """
    通过id获取行政级别
    :param id: 行政级别id
    :return: 行政级别对象
    """
    _sql_db = SQLlite3DB()
    # 封装查询参数字典
    param_dict = {"id": id}
    _administrative_level = AdministrativeLevel()
    _result = _sql_db.select_one(_administrative_level, param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    _administrative_level.id = _result[0]
    _administrative_level.name = _result[1]
    return _administrative_level

def save_or_find_level_by_name(name) -> AdministrativeLevel:
    """
    添加或者查询行政级别
    :param name: 行政级别名称
    :return:  行政级别
    """
    administrativeLevel = find_administrative_level_by_name(name)
    if administrativeLevel is None:
        administrativeLevel = AdministrativeLevel()
        administrativeLevel.name = name
        administrativeLevel = save(administrativeLevel)
    return administrativeLevel

def find_administrative_level_by_name(name) -> AdministrativeLevel:
    """
    通过名称获取行政级别
    :param name: 行政级别名称
    :return: 行政级别
    """
    _sql_db = SQLlite3DB()
    # 封装查询参数字典
    _param_dict = {"name": name}
    _administrative_level = AdministrativeLevel()
    _result = _sql_db.select_one(_administrative_level, _param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    _administrative_level.id = _result[0]
    _administrative_level.name = _result[1]
    return _administrative_level


def save(administrativeLevel) -> AdministrativeLevel:
    """
    添加行政级别
    :param administrativeLevel: 行政级别对象
    :return: 行政级别
    """
    _sql_db = SQLlite3DB()
    _id = _sql_db.insert(administrativeLevel)
    administrativeLevel.id = _id
    # 关闭连接
    _sql_db.close()
    return administrativeLevel


def create_table():
    """
    创建行政级别表
    """
    _sql_db = SQLlite3DB()
    _sql_db.create_table(AdministrativeLevel(), "id")
