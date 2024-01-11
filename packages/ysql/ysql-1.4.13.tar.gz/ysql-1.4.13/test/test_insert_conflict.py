# -*- coding:utf-8 -*-
import os
import sqlite3
from dataclasses import dataclass
from typing import Optional

import pytest
from ysql import Entity, Constraint as cs, Dao, DaoFunc, Insert, MetaDatabase
from ysql.dao import Conflict, Sql


@Entity(check_type=True)
@dataclass
class Student:
    name: str = cs.unique
    age: int = None
    id: int = cs.auto_primary_key


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):

    @Insert(conflict=Conflict.error)
    def insert_error(self):
        pass

    @Insert(conflict=Conflict.ignore)
    def insert_ignore(self):
        pass

    @Insert(conflict=Conflict.replace)
    def insert_replace(self):
        pass

    @Sql("select * from __ where name=? limit 1;")
    def get_student_by_name(self, name) -> Optional[Student]:
        pass


class Database(MetaDatabase):
    dao_student = DaoStudent()


students = [Student(name='张三', age=10),
            Student(name='张三', age=11),
            Student(name='李四', age=12)]


def init_db() -> Database:
    db_path = f"db_folder/{os.path.basename(__file__).split('.')[0]}.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database(db_path)
    db.connect()
    db.create_tables()
    return db


def test_insert_default():
    db = init_db()
    with pytest.raises(sqlite3.IntegrityError) as exc_info:
        for student in students:
            db.dao_student.insert(student)
    assert "UNIQUE constraint failed" in str(exc_info.value)
    db.rollback()
    db.disconnect()


def test_insert_error():
    db = init_db()
    with pytest.raises(sqlite3.IntegrityError) as exc_info:
        for student in students:
            db.dao_student.insert_error(student)
    assert "UNIQUE constraint failed" in str(exc_info.value)
    db.rollback()
    db.disconnect()


def test_insert_ignore():
    db = init_db()
    for student in students:
        db.dao_student.insert_ignore(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == select_student.age
    db.disconnect()


def test_insert_replace():
    db = init_db()
    for student in students:
        db.dao_student.insert_replace(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == students[1].age
    db.disconnect()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
