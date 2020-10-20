from db.sql_exception import SQLException
from model.administrative_level import AdministrativeLevel
from util.transition import hump_to_underline


def select_sql(noneObj, param_dict) -> str:
    """
    封装查询sql语句
    :param noneObj 空对象
    :param param_dict 查询参数字典
    :return 查询的shql语句
    """
    # 判断参数字典是否为空
    if param_dict is None:
        raise SQLException("查询参数字典不能为空！")
    # 判断参数字典是否为字典类型
    if not isinstance(param_dict, dict):
        raise SQLException("查询参数字典应该为字典类型，当前类型为：" + str(type(param_dict)))
    # 获取类名称并且将驼峰命名改为下划线命名 让实体类与数据库一致
    clazz_name = hump_to_underline(type(noneObj).__name__)
    # 封装查询sql语句
    sql = "SELECT "
    # 遍历实体属性字典
    for attribute in noneObj.__dict__:
        sql = sql + clazz_name + "." + hump_to_underline(attribute) + ", "
    sql = sql[:-2] + " FROM " + clazz_name + " WHERE "
    for param in param_dict:
        sql = sql + clazz_name + "." + param + "= '" + str(param_dict.get(param)) + "' AND "
    return sql[:-4]


def delete_sql(clazz, param_dict) -> str:
    """
    封装删除sql语句
    :param clazz 类
    :param param_dict 参数字典
    :return 删除的sql语句
    """
    # 获取类名称并且将驼峰命名改为下划线命名 让实体类与数据库一致
    clazz_name = hump_to_underline(clazz.__name__)
    # 封装删除sql语句
    sql = "DELETE FROM " + clazz_name + " WHERE "
    for param in param_dict:
        sql = sql + clazz_name + "." + param + "= '" + str(param_dict.get(param)) + "' AND"
    return sql[:-3]


def delete_sql(obj) -> str:
    """
    封装删除sql语句
    :param obj 对象
    :return 删除的sql语句
    """
    clazz_name = hump_to_underline(obj.__class__.__name__)
    # 封装删除sql语句
    sql = "DELETE FROM " + clazz_name + " WHERE "
    for attribute_name in obj.__dict__:
        sql = sql + clazz_name + "." + attribute_name + "= '" + str(obj.__getattribute__(attribute_name)) + "' AND"
    return sql[:-3]


def update_sql(clazz, updata_dict, condition_dict) -> str:
    """
    封装更新sql语句
    :param clazz 类
    :param updata_dict 更新的参数字典
    :param 条件字典
    :return 更新的sql语句
    """
    clazz_name = hump_to_underline(clazz.__name__)
    sql = "UPDATE " + clazz_name + " SET "
    if updata_dict is None:
        raise SQLException("更新字典不能为空！")
    for args in updata_dict:
        if updata_dict.get(args) is not None:
            sql = sql + args + " = " + str(updata_dict.get(args)) + " , "
    sql = sql[:-2]
    if condition_dict is None:
        raise SQLException("条件字典不能为空！")
    sql = sql + "WHERE "
    for condition in condition_dict:
        sql = sql + condition + " = '" + str(condition_dict.get(condition)) + "' AND "
    return sql[:-4]


def update_sql(obj, condition_dict) -> str:
    """
    封装更新sql语句
    :param obj 对象
    :param condition_dict 条件字典
    :return 更新的sql语句
    """
    clazz_name = hump_to_underline(obj.__class__.__name__)
    sql = "UPDATE " + clazz_name + " SET "
    for attribute_name in obj.__dict__:
        if obj.__getattribute__(attribute_name) is not None:
            sql = sql + attribute_name + " = '" + str(obj.__getattribute__(attribute_name)) + "' ,"
    sql = sql[:-1] + "WHERE "
    if condition_dict is None:
        raise SQLException("条件字典不能为空！")
    for condition in condition_dict:
        sql = sql + condition + " = '" + str(condition_dict.get(condition)) + "' AND "
    return sql[:-4]


def insert_sql(clazz, param_dict):
    """
    封装插入sql语句
    :param clazz 类
    :param param_dict 添加的参数字典
    :return 插入的sqhl语句
    """
    # 获取类名称并且转成下划线命名
    clazz_name = hump_to_underline(clazz.__name__)
    # 封装sql语句，并且前后封装同时进行
    sql = "INSERT INTO " + clazz_name + "( "
    sql_two = ") VALUES ("
    for param in param_dict:
        if param_dict.get(param) is not None:
            sql = sql + clazz_name + "." + param + " ,"
            sql_two = sql_two + "'" + str(param_dict.get(param)) + "'"
    # 整合sql语句
    sql = sql[:-1] + sql_two + ")"
    return sql


def insert_sql(obj):
    """
    封装插入sql语句
    :param 对象
    :return 插入的sql语句
    """
    clazz_name = hump_to_underline(obj.__class__.__name__)
    sql = "INSERT INTO " + clazz_name + "( "
    sql_two = ") VALUES ("
    for attribute_name in obj.__dict__:
        if obj.__getattribute__(attribute_name) is None:
            continue
        if attribute_name == "id":
            if obj.__getattribute__(attribute_name) == 0:
                continue
        sql = sql  + attribute_name + " ,"
        sql_two = sql_two + "'" + str(obj.__getattribute__(attribute_name)) + "' ,"



    sql = sql[:-1] + sql_two[:-1] + ")"
    return sql


def create_table(obj, key_name):
    """
    封装创建表sql
    :param obj: 对象
    :param key_name: 主键名称
    :return: 创建的sql
    """
    clazz_name = hump_to_underline(obj.__class__.__name__)
    sql = "CREATE TABLE IF NOT EXISTS " + clazz_name + " ( "
    for attribute_name in obj.__dict__:
        sql = sql + attribute_name
        if isinstance(obj.__getattribute__(attribute_name), int):
            sql = sql + " INTEGER , "
        if isinstance(obj.__getattribute__(attribute_name), str):
            sql = sql + " TEXT , "
        if key_name == attribute_name:
            sql = sql[:-2]
            sql = sql + "NOT NULL PRIMARY KEY AUTOINCREMENT , "
    sql = sql[:-2] + ")"
    return sql


if __name__ == '__main__':
    a = AdministrativeLevel()
    print(create_table(a, "id"))
