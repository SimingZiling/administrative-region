from db.sqllie3.sqllite3_db import SQLlite3DB
from model.administrative_division import AdministrativeDivision


def create_table():
    """
    创建行政区划表
    """
    _sql_db = SQLlite3DB()
    _sql_db.create_table(AdministrativeDivision(), "id")


def find_administrative_division_by_id(id) -> AdministrativeDivision:
    """
    通过id获取行政区划
    :param id: 行政区划id
    :return: 行政区划对象
    """
    _sql_db = SQLlite3DB()
    # 封装参数字典
    param_dict = {"id": id}
    _administrative_division = AdministrativeDivision()
    _result = _sql_db.select_one(_administrative_division, param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    return _package(_administrative_division, _result)


def find_administrative_division_by_name(name) -> AdministrativeDivision:
    """
    通过名称获取行政区划
    :param name: 名称
    :return: 行政区划对象
    """
    _sql_db = SQLlite3DB()
    # 封装参数字典
    param_dict = {"name": name}
    _administrative_division = AdministrativeDivision()
    _result = _sql_db.select_one(_administrative_division, param_dict)
    # 关闭连接
    _sql_db.close()
    if _result is None:
        return None
    return _package(_administrative_division, _result)

def save(administrativeDivision) -> AdministrativeDivision:
    """
    添加行政区划
    :param administrativeDivision: 行政区划对象
    :return: 行政区划
    """
    _sql_db = SQLlite3DB()
    _id = _sql_db.insert(administrativeDivision)
    administrativeDivision.id = _id
    # 关闭连接
    _sql_db.close()
    return administrativeDivision

def _package(_obj, _result):
    """
    封装行政区划
    :param obj: 空对象
    :param result: 结果
    :return: 行政区划对象
    """
    _obj.id = _result[0]
    _obj.name = _result[1]
    _obj.administrative_level_id = _result[2]
    _obj.administrative_type_id = _result[3]
    _obj.administrative_code = _result[4]
    _obj.parent_administrative_division_id = _result[5]
    return _obj

