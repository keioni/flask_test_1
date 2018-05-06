# -*- coding: utf-8 -*-

import time

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from orm.security import secure_hashing, generate_auth_code
from cyreco.sys.config import conf


engine = create_engine('sqlite:///userlist.sqlite3', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class UsersAuthData(Base):
    __tablename__ = 'users_authdata'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(32), unique=True)
    mailaddr = Column('mailaddr', String(254), unique=True)
    password = Column('password', String(44))
    valid = Column('valid', Boolean)
    create_time = Column('create_time', Integer)
    last_login = Column('last_login', Integer)

    def __init__(self, name: str, mailaddr: str, plain_password: str):
        self.name = name
        self.mailaddr = mailaddr
        self.password = secure_hashing(plain_password, conf.salt)
        self.valid = False
        self.create_time = self.last_login = int(time.time())

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "name='{}'".format(self.name),
            "mailaddr='{}'".format(self.mailaddr),
            "password='{}'".format(self.password),
            "valid='{}'".format(self.valid),
            "create_time={}".format(self.create_time),
            "last_login={}".format(self.last_login),
        ])
        return "<UsersAuthData({})".format(repr_args)


class UsersProfile(Base):
    __tablename__ = 'users_profile'

    id = Column('id', Integer, primary_key=True)
    friendly_name = Column('friendly_name', String)

    def __init__(self, user_id: int):
        self.id = user_id

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
        ])
        return "<UsersProfile({})".format(repr_args)


class UsersValidation(Base):
    __tablename__ = 'users_validation'

    id = Column('id', Integer, primary_key=True)
    mailaddr = Column('mailaddr', String(254), unique=True)
    auth_code = Column('auth_code', String(8))
    expire_time = Column('expire_time', Integer)

    def __init__(self, user_id: int, mailaddr: str, auth_code: str):
        self.id = user_id
        self.mailaddr = mailaddr
        self.auth_code = auth_code
        self.expire_time = int(time.time()) + 3600

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format(self.id),
            "mailaddr='{}'".format(self.mailaddr),
            "auth_code='{}'".format(self.auth_code),
            "expire_time={}".format(self.expire_time),
        ])
        return "<UsersValidation({})".format(repr_args)


# class UsersExtraInfo(Base):
#     __tablename__ = 'users_extrainfo'
#     pass


# class UsersRecord(Base):
#     __tablename__ = 'users_record'
#     pass
