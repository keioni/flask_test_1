# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

class UserDatabase():
    db_users = 'sqlite:///mogmog/users.sqlite3'
    meta = MetaData()
    table_users = Table('users', meta,
                        Column('idx', Integer),
                        Column('username', String),
                        Column('hashed_password', String),
                       )

    def __init__(self):
        self.engine = create_engine(UserDatabase.db_users)
        self.conn = self.engine.connect()

    def query_userdata(self, username: str) -> tuple:
        t = self.table_users.c
        s = select([t.name, t.password]).where(t.username == username)
        for row in self.conn.execute(s):
            return (row.username, row.hashed_password)

    def add_user(self, user: dict):
        ins = self.table_users.insert().values( # pylint: disable=E1120
            idx=user['idx'],
            username=user['username'],
            hashed_password=user['hashed_password'],
        )
        result = self.conn.execute(ins)
        result.close()
