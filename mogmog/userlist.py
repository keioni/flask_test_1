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

    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.meta = MetaData()
        self.userlist = Table('userlist', self.meta,
            Column('id', Integer, primary_key=True),
            Column('username', String),
            Column('hashed_password', String),
        )
        self.salt = os.environ.get('BLAKE2B_SALT')
 
    def hash_password(self, password: str) -> str:
        h = blake2b(key=self.salt, digest_size=32)
        h.update(password.encode('utf-8'))
        return b64encode(h.digest()).decode()

    def authenticate_user(self, username: str, password: str) -> bool:
        db_username, db_hashed_password = self.query_userdata(username)
        if db_username:
            return compare_digest(
                self.hash_password(password),
                db_hashed_password
            )
        else:
            return False

    def query_userdata(self, username: str) -> tuple:
        t = self.userlist.c
        result = self.userlist.select([t.username, t.password]).where(t.username == username)
        for row in result:
            result.close()
            return (row.username, row.hashed_password)
        result.close()
        return ()

    def add_user(self, user: dict):
        ins = self.userlist.insert().values( # pylint: disable=E1120
            username=user['username'],
            hashed_password=user['hashed_password'],
        )
        conn = self.engine.connect()
        result = conn.execute(ins)
        result.close()
