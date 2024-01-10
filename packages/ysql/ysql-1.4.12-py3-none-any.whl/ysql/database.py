# -*- coding: utf-8 -*-
import os
import sqlite3
from typing import Optional, Any


# ====================================================================================================================
class MetaDatabase:
    """元数据库类，提供库级的操作。

    由于元编程无法使用代码提示，因此采取继承写法。

    Example:
        @Entity
        @dataclass
        class Student:  # 定义一个数据类
            name: str
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:  # 定义一个数据访问类

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass

        class Database(MetaDatabase):  # 定义一个数据库类，继承元数据库类
            dao1 = DaoStudent()  # 将各个数据访问类实例化为类中静态变量，集中管理，统一对外。
            dao2 = ...
            dao3 = ...

        db = Database(db_path='test0.db')  # 实例化数据库类，并传入数据库路径
        db.connect()  # 连接数据库
        db.create_tables()  # 创建数据表

    """

    # ================================================================================================================
    # 可直接调用的方法
    def connect(self, use_multithreading=False):
        """连接数据库"""
        self.__check_path(self.db_path)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=not use_multithreading)
        self.cursor = self.connection.cursor()
        self.__update_cursor()

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()

    def create_tables(self):
        """当表不存在时，才会创建数据表。因此可以反复调用该方法，而不会产生错误。"""
        for dao in self.dao_list:
            dao._create_table()  # noqa
        self.commit()

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    def execute(self, sql: str, args: Optional[tuple[Any, ...]] = None):
        """给外部提供的直接执行sql的接口，避免了再调用内部的connection"""
        if args:
            self.connection.execute(sql, args)
        else:
            self.connection.execute(sql)

    # ================================================================================================================
    # 内部方法
    def __new__(cls, *args, **kwargs):
        # 获取子类的所有属性
        subclass_attrs = dir(cls)
        # 初步筛选静态变量（不包括方法和特殊属性）
        static_attrs = [attr for attr in subclass_attrs
                        if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        # 根据是否具有entity属性筛选出最终dao属性
        dao_list = [getattr(cls, attr) for attr in static_attrs
                    if hasattr(getattr(cls, attr), "entity")
                    and hasattr(getattr(cls, attr), "update_cursor")]
        # 赋值dao_list为类属性，以便在类内部可见
        cls.dao_list = dao_list

        return super().__new__(cls)

    def __init__(self, db_path: str):
        self.connection = None
        self.cursor = None
        self.db_path = db_path

    # ================================================================================================================
    # 类内方法
    def __update_cursor(self):
        for dao in self.dao_list:
            dao.update_cursor(cursor=self.cursor)

    @staticmethod
    def __check_path(path):
        """检查并确保目录存在"""
        db_folder = os.path.dirname(path)
        if db_folder != '' and not os.path.exists(db_folder):
            os.makedirs(db_folder, exist_ok=True)
