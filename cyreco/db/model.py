# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column, Integer, String, Boolean, LargeBinary

from cyreco.db import engine, Base
from cyreco.utils.security import secure_hashing, generate_auth_code
from cyreco.sys.config import CONF

class UsersAuthData(Base):
    __tablename__ = 'users_authdata'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(32), unique=True)
    mailaddr = Column('mailaddr', String(254), unique=True)
    password = Column('password', String(44))
    is_valid = Column('is_valid', Boolean)
    is_active = Column('is_active', Boolean)
    create_time = Column('create_time', Integer)
    last_login = Column('last_login', Integer)

    def __init__(self, name: str,  plain_password: str, mailaddr: str):
        self.name = name
        self.mailaddr = mailaddr
        self.password = secure_hashing(plain_password, CONF.salt)
        self.is_valid = False
        self.is_active = True
        self.create_time = self.last_login = int(time.time())

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "name='{}'".format(self.name),
            "mailaddr='{}'".format(self.mailaddr),
            "password='{}'".format(self.password),
            "is_valid='{}'".format(self.is_valid),
            "is_active='{}'".format(self.is_active),
            "create_time={}".format(self.create_time),
            "last_login={}".format(self.last_login),
        ])
        return "<UsersAuthData({})".format(repr_args)


class UsersProfile(Base):
    __tablename__ = 'users_profile'

    name = Column('name', String(32), primary_key=True)
    friendly_name = Column('friendly_name', String)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
        ])
        return "<UsersProfile({})".format(repr_args)


class UsersValidation(Base):
    __tablename__ = 'users_validation'

    name = Column('name', String(32), primary_key=True)
    mailaddr = Column('mailaddr', String(254), unique=True)
    auth_code = Column('auth_code', String(8))
    expire_time = Column('expire_time', Integer)

    def __init__(self, name: str, mailaddr: str, auth_code: str):
        times_to_expire = CONF.validation_timeout_in_sec
        self.name = name
        self.mailaddr = mailaddr
        self.auth_code = auth_code
        self.expire_time = time.time() + int(times_to_expire)

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
            "mailaddr='{}'".format(self.mailaddr),
            "auth_code='{}'".format(self.auth_code),
            "expire_time={}".format(self.expire_time),
        ])
        return "<UsersValidation({})".format(repr_args)


# class UsersExtraInfo(Base):
#     __tablename__ = 'users_extrainfo'
#     pass


class UsersRecord(Base):
    __tablename__ = 'users_record'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    record_id = Column('record_id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(32), index=True)
    record_caption = Column('record_caption', String(64))
    last_update = Column('last_update', Integer)
    record_count = Column('record_count', Integer)
    record_data = Column('record_data', LargeBinary(200))

    def __init__(self, name: str, record_caption: str):
        self.name = name
        self.record_caption = record_caption
        self.last_update = 0
        self.record_count = 0
        self.record_data = b''

    def __repr__(self):
        repr_args = ', '.join([
            "record_id={}".format(self.record_id),
            "name='{}'".format(self.name),
            "record_caption='{}'".format(self.record_caption),
            "last_update={}".format(self.last_update),
            "record_count={}".format(self.record_count),
            "record_data=b'{}'".format(self.record_data),
        ])
        return "<UsersRecord({})".format(repr_args)


class UsersRecordArchives(Base):
    __tablename__ = 'users_record_archive'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    record_id = Column('archive_id', Integer, primary_key=True)
    record_count = Column('record_count', Integer)
    record_data = Column('record_data', LargeBinary(60000))

    def __init__(self, name: str, record_id: int):
        self.record_id = record_id
        self.record_count = 0
        self.record_data = b''

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
            "record_caption='{}'".format(self.record_caption),
            "record_data=b'{}'".format(self.record_data),
        ])
        return "<UsersRecordArchive({})".format(repr_args)
