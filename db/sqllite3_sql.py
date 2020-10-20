from db.sql_exception import SQLException
from model.administrative_level import AdministrativeLevel
from model.administrative_type import AdministrativeType
from util.transition import hump_to_underline


def select_sql(clazz, args_dict) -> str:
    """封装查询sql语句"""
    # 判断参数字典是否为空
    if args_dict is None:
        raise SQLException("查询参数字典不能为空！")
    # 判断参数字典是否为字典类型
    if not isinstance(args_dict, dict):
        raise SQLException("查询参数字典应该为字典类型，当前类型为：" + str(type(args_dict)))
    # 获取类名称并且将驼峰命名改为下划线命名 让实体类与数据库一致
    clazz_name = hump_to_underline(type(clazz).__name__)
    # 封装查询sql语句
    sql = "SELECT "
    # 遍历实体属性字典
    for attribute in clazz.__dict__:
        sql = sql + clazz_name + "." + hump_to_underline(attribute) + ", "
    sql = sql[:-2] + " FROM " + clazz_name + " WHERE "
    for args in args_dict:
        sql = sql + clazz_name + "." + args + "= '" + str(args_dict.get(args)) + "' AND "
    return sql[:-4]


def delete_sql(clazz, args_dict) -> str:
    """封装删除sql语句"""
    # 获取类名称并且将驼峰命名改为下划线命名 让实体类与数据库一致
    clazz_name = hump_to_underline(type(clazz).__name__)
    # 封装删除sql语句
    sql = "DELETE FROM " + clazz_name + " WHERE "
    for args in args_dict:
        sql = sql + clazz_name + "." + args + "= '" + str(args_dict.get(args)) + "' AND"
    return sql[:-3]


def delete_sql(obj) -> str:
    """封装删除sql语句"""
    clazz_name = hump_to_underline(obj.__class__.__name__)
    # 封装删除sql语句
    sql = "DELETE FROM " + clazz_name + " WHERE "
    for attribute_name in obj.__dict__:
        sql = sql + clazz_name + "." + attribute_name + "= '" + str(obj.__getattribute__(attribute_name)) + "' AND"
    return sql[:-3]


def update_sql(clazz, updata_dict, condition_dict) -> str:
    """封装更新sql语句"""
    clazz_name = hump_to_underline(type(clazz).__name__)
    sql = "UPDATE " + clazz_name + " SET "
    if updata_dict is None:
        raise SQLException("更新字典不能为空！")
    for args in updata_dict:
        sql = sql + args + " = " + str(updata_dict.get(args)) + " , "
    sql = sql[:-2]
    if condition_dict is None:
        raise SQLException("条件字典不能为空！")
    sql = sql + "WHERE "
    for condition in condition_dict:
        sql = sql + condition + " = '" + str(updata_dict.get(condition)) + "' AND "
    return sql[:-4]


def update_sql(obj, condition) -> str:
    """封装更新sql语句"""
    clazz_name = hump_to_underline(obj.__class__.__name__)
    sql = "UPDATE " + clazz_name + " SET "
    for attribute_name in obj.__dict__:
        sql = sql + attribute_name + " = '" + str(obj.__getattribute__(attribute_name)) + "' ,"
    sql = sql[:-1] + "WHERE "
    if isinstance(condition, list):
        for c in condition:
            sql = sql + c + " = '" + str(obj.__getattribute__(c)) + "' AND "
        return sql[:-4]
    else:
        sql = sql + condition + " = '" + str(obj.__getattribute__(condition)) + "' "
        return sql


def insert_sql(clazz, args_dict):
    """封装添加sql语句"""
    clazz_name = hump_to_underline(type(clazz).__name__)
    sql = "INSERT INTO " + clazz_name + "( "
    sql_two = ") VALUES ("
    for args in args_dict:
        sql = sql + clazz_name + "." + args+" ,"
        sql_two = sql_two + "'" + str(args_dict.get(args)) +"'"
    sql = sql[:-1]+sql_two+")"
    return sql


def insert_sql(obj):
    # TODO 判断空语句
    """封装添加sql语句"""
    clazz_name = hump_to_underline(obj.__class__.__name__)
    sql = "INSERT INTO " + clazz_name + "( "
    sql_two = ") VALUES ("
    for attribute_name in obj.__dict__:
        sql = sql + clazz_name + "." + attribute_name + " ,"
        sql_two = sql_two + "'" + str(obj.__getattribute__(attribute_name)) + "'"
    sql = sql[:-1] + sql_two + ")"
    return sql

if __name__ == '__main__':
    # a = {'id': 1, 'name': "国"}
    a = AdministrativeLevel(id=1, name="国")
    c = AdministrativeType(id=1,name="国家")
    print(insert_sql(c))
