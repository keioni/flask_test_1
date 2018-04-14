# -*- coding: utf-8 -*-
"""
    Flask-Login user management module for my study program.

    by Kei Onimaru <otegami@devel.keys.jp>
"""

from flask_login import LoginManager
from flask_login import UserMixin

from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String, DATETIME, BOOLEAN
from sqlalchemy.sql import select

import os
from hashlib import blake2b # pylint: disable=E0611
from hmac import compare_digest
from base64 import b64decode, b64encode


class LoginUser(UserMixin):

    def __init__(self, username: str):
        self.username = username

    def get_id(self) -> str:
        return self.username


class UserList():
    meta = MetaData()
    userlist = Table('userlist', meta,
        Column('id', Integer, primary_key=True),
        Column('username', String),
        Column('hashed_password', String),
        Column('register_date', DATETIME),
    )

    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.salt = os.environ.get('BLAKE2B_SALT').encode('utf-8')

    def hash_password(self, password: str) -> str:
        h = blake2b(key=self.salt, digest_size=32)
        h.update(password.encode('utf-8'))
        return b64encode(h.digest()).decode()

    def query_userdata(self, username: str) -> tuple:
        ret: tuple
        tbl = self.userlist
        query = tbl.select().where(tbl.c.username == username)
        conn = self.engine.connect()
        result = conn.execute(query)
        for row in result:
            ret = (row.username, row.hashed_password)
        else:
            ret = (None, None)
        conn.close()
        return ret

    def execute_statement(self, statement):
        ret: bool
        conn = self.engine.connect()
        result = conn.execute(statement)
        if result.rowcount:
            ret = True
        else:
            ret = False
        conn.close()
        return ret

    def auth_user(self, username: str, password: str) -> bool:
        ret: bool
        db_username, db_hashed_password = self.query_userdata(username)
        if db_username:
            ret = compare_digest(
                self.hash_password(password),
                db_hashed_password
            )
        else:
            ret = False
        return ret

    def add_user(self, username: str, password: str) -> bool:
        ret: bool
        hashed_password = self.hash_password(password)
        stmt = self.userlist.insert().values( # pylint: disable=E1120
            username=username,
            hashed_password=hashed_password,
        )
        ret = self.execute_statement(stmt)
        # conn = self.engine.connect()
        # result = conn.execute(stmt)
        # if result.rowcount:
        #     ret = True
        # else:
        #     ret = False
        # conn.close()
        return ret

    def delete_user(self, username: str) -> bool:
        ret: bool
        tbl = self.userlist
        db_username, _ = self.query_userdata(username)
        if db_username:
            stmt = tbl.delete().where(tbl.c.username == username) # pylint: disable=E1120
            ret = self.execute_statement(stmt)
            # conn = self.engine.connect()
            # result = conn.execute(stmt)
            # if result.rowcount:
            #     ret = True
            # else:
            #     ret = False
            # conn.close()
        else:
            ret = False
        return ret

class UserMailAddressList():
    meta = MetaData()
    userlist = Table('user_mailaddr_list', meta,
        Column('id', Integer, primary_key=True),
        Column('masked_mailaddr', String),
        Column('hashed_mailaddr', String),
        Column('reset_code', String),
        Column('reseting_date', DATETIME),
    )
