# -*- coding:utf-8 -*-
import os
from dataclasses import dataclass

import pytest

from ysql.dao import Dao, Sql, DaoFunc
from ysql.database import MetaDatabase
from ysql.entity import Entity, Constraint as cs


@Entity(check_type=True)
@dataclass
class Student:
    name: str
    age: int
    id: int = cs.auto_primary_key


@Dao(entity=Student)
class DaoStudent(DaoFunc):

    @Sql("delete from student where id=?;")
    def delete_student_by_id(self, student_id):
        pass


@Entity(check_type=True)
@dataclass
class Score:
    score: float
    student_id: int = cs.primary_key, cs.foreign_key(parent_entity=Student,
                                                     parent_field='id',
                                                     delete_link=cs.cascade)


@Dao(entity=Score)
class DaoScore(DaoFunc):

    @Sql(f"select * from __ where student_id=?;")
    def get_score_by_student_id(self, student_id):
        pass


class Database(MetaDatabase):
    dao_student = DaoStudent()
    dao_score = DaoScore()


@pytest.fixture(scope="module")
def init_db() -> Database:
    db_path = f"db_folder/{os.path.basename(__file__).split('.')[0]}.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database(db_path)
    db.connect()
    db.execute("PRAGMA foreign_keys = ON;")
    db.create_tables()
    yield db
    db.disconnect()


students = [Student(name='张三', age=10),
            Student(name='张三', age=11),
            Student(name='李四', age=12)]


def test_insert_data(init_db: Database):
    db = init_db
    db.dao_student.insert(students)


def test_foreign_key_delete_cascade(init_db: Database):
    """外键"""
    db = init_db
    select_id = 1
    score = Score(150.0, student_id=select_id)
    db.dao_score.insert(score)
    db.dao_student.delete_student_by_id(student_id=select_id)
    db.commit()
    result = db.dao_score.get_score_by_student_id(select_id)
    assert len(result) == 0


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
