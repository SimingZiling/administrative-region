import sqlite3
from configparser import NoOptionError, NoSectionError

from db.sql_exception import SQLException
from db.sqllie3 import sqllite3_sql
from util.config import get_config


class SQLlite3DB(object):

    def __init__(self):
        try:
            self._name = get_config("sqllite3", "name")
        except NoOptionError:
            raise SQLException("配置文件中name参数不存在或参数名错误！")
        except NoSectionError:
            raise SQLException("配置文件中sqllite3模块不存在或者模块名称错误")
        # 获取数据库连接
        self._connect = sqlite3.connect(self._name)
        # 获取游标
        self._cursor = self._connect.cursor()

    def close(self):
        """关闭数据库连接"""
        # 当连接存在时关闭连接
        if self._connect is not None:
            self._connect.close()

    def select_one(self, noneObj, param_dict):
        """
        进行查询操作
        :param noneObj: 空对象
        :param param_dict: 查询参数
        :return: 结果集
        """
        sql = sqllite3_sql.select_sql(noneObj, param_dict)
        return self.select_one_sql(sql)

    def select_one_sql(self, sql):
        """
        进行查询操作
        :param sql: sql语句
        :return: 结果集
        """
        result_set = self._cursor.execute(sql).fetchone()
        # 提交事务
        self._connect.commit()
        # 关闭数据库连接
        return result_set

    def select_list(self, noneObj, param_dict):
        """
        进行查询列表操作
        :param noneObj: 空对象
        :param param_dict: 查询参数
        :return: 结果集
        """
        sql = sqllite3_sql.select_sql(noneObj, param_dict)
        return self.select_list_sql(sql)

    def select_list_sql(self, sql):
        """
        进行查询列表操作
        :param sql: sql语句
        :return: 结果集
        """
        result_set = self._cursor.execute(sql).fetchall()
        # 提交事务
        self._connect.commit()
        # 关闭数据库连接
        return result_set

    def insert_sql(self, sql):
        """
        插入数据
        :param sql: sql语句
        :return: 主键
        """
        result = self._cursor.execute(sql).lastrowid
        self._connect.commit()
        return result

    def insert(self,obj):
        sql = sqllite3_sql.insert_sql(obj)
        return self.insert_sql(sql)

    def create_table_sql(self, sql):
        """
        创建表
        :param sql: sql语句
        """
        self._cursor.execute(sql)
        self._connect.commit()

    def create_table(self, obj, key_name):
        """
        创建表
        :param obj: 对象
        :param key_name: 主键名
        """
        sql = sqllite3_sql.create_table(obj, key_name)
        self.create_table_sql(sql)
