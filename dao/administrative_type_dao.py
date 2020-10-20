from db.sqllie3.sqllite3_db import SQLlite3DB
from model.administrative_type import AdministrativeType


def find_administrative_type_by_name(name) -> AdministrativeType:
    """
    通过名称获取行政类型
    :param name: 行政类型名称
    :return: 行政类型对象
    """
    _sql_db = SQLlite3DB()
    # 封装查询参数字典
    param_dict = {"name": name}
    _administrative_tpye = AdministrativeType()
    _result = _sql_db.select_one(_administrative_tpye, param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    return _package(_administrative_tpye, _result)


def find_administrative_type_by_id(id) -> AdministrativeType:
    """
    通过id获取行政类型
    :param name: 行政类型名称
    :return: 行政类型对象
    """
    _sql_db = SQLlite3DB()
    # 封装查询参数字典
    param_dict = {"id": id}
    _administrative_tpye = AdministrativeType()
    _result = _sql_db.select_one(_administrative_tpye, param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    return _package(_administrative_tpye, _result)


def save_or_find_type_by_name(name) -> AdministrativeType:
    """
    通过名称添加或者查询行政类型
    :param name: 行政类型名称
    :return: 行政类型
    """
    administrativeType = find_administrative_type_by_name(name)
    if administrativeType is None:
        administrativeType = AdministrativeType()
        administrativeType.name = name
        administrativeType = save(administrativeType)
    return administrativeType


def save(administrativeType) -> AdministrativeType:
    """
    添加行政类型
    :param administrativeType: 行政类型对象
    :return: 行政类型
    """
    _sql_db = SQLlite3DB()
    _id = _sql_db.insert(administrativeType)
    administrativeType.id = _id
    # 关闭连接
    _sql_db.close()
    return administrativeType


def create_table():
    """
    创建行政类型表
    """
    _sql_db = SQLlite3DB()
    _sql_db.create_table(AdministrativeType(), "id")


def _package(_obj, _result):
    """
    封装行政类型
    :param _obj: 空对象
    :param _result: 结果
    :return: 行政类型对象
    """
    _obj.id = _result[0]
    _obj.name = _result[1]
    return _obj
