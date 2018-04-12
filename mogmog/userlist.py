# -*- coding: utf-8 -*-
"""
    Flask-Login user management module for my study program.

    by Kei Onimaru <otegami@devel.keys.jp>
"""

from flask_login import LoginManager
from flask_login import UserMixin

from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

class LoginUser(UserMixin):

    def __init__(self, username: str):
        self.username = username

    def get_id(self) -> str:
        return self.username


class UserList():
    db_userlist = 'sqlite:///mogmog/userlist.sqlite3'
    meta = MetaData()
    userlist = Table('userlist', meta,
        Column('idx', Integer),
        Column('username', String),
        Column('hashed_password', String),
    )

    def __init__(self):
        self.engine = create_engine(UserList.db_userlist)
        self.conn = self.engine.connect()

    def authenticate(self, username: str, password: str) -> bool:
        if username == 'test' and password == 'test':
            return True
        else:
            return False

    def query_userdata(self, username: str) -> tuple:
        t = self.userlist.c
        s = select([t.name, t.password]).where(t.username == username)
        for row in self.conn.execute(s):
            return (row.username, row.hashed_password)

    def add_user(self, user: dict):
        ins = self.userlist.insert().values( # pylint: disable=E1120
            idx=user['idx'],
            username=user['username'],
            hashed_password=user['hashed_password'],
        )
        result = self.conn.execute(ins)
        result.close()
