# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Binary
from datetime import datetime

from cyreco.db import Base
from cyreco.utils.security import secure_hashing, generate_auth_code
from cyreco.sys.config import CONF


class CyUserAuth(Base):
    __tablename__ = 'users_authdata'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB',
    #     'mysql_charset': 'utf8mb4',
    # }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(24), unique=True, nullable=False)
    mailaddr = Column('mailaddr', String(254), unique=True, nullable=False)
    password = Column('password', String(44), nullable=False)
    is_valid = Column('is_valid', Boolean)
    is_active = Column('is_active', Boolean)
    create_time = Column('create_time', DateTime)
    # last_login = Column('last_login', DateTime)

    def __init__(self, name: str,  plain_password: str, mailaddr: str):
        self.name = name
        self.mailaddr = mailaddr
        self.password = secure_hashing(plain_password, CONF.salt)
        self.is_valid = False
        self.is_active = True
        self.create_time = datetime.now()
        # self.last_login = datetime.now()

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "name='{}'".format(self.name),
            "mailaddr='{}'".format(self.mailaddr),
            "password='{}'".format(self.password),
            "is_valid='{}'".format(self.is_valid),
            "is_active='{}'".format(self.is_active),
            "create_time='{}'".format(self.create_time),
            # "last_login={}".format(self.last_login),
        ])
        return "<CyUsersAuth({})".format(repr_args)


class CyUserProfile(Base):
    __tablename__ = 'users_profile'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB',
    #     'mysql_charset': 'utf8mb4',
    # }

    name = Column('name', String(24), primary_key=True)
    friendly_name = Column('friendly_name', String)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
        ])
        return "<CyUserProfile({})".format(repr_args)


class CyUserValidate(Base):
    __tablename__ = 'users_validation'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB',
    #     'mysql_charset': 'utf8mb4',
    # }

    name = Column('name', String(24), primary_key=True)
    mailaddr = Column('mailaddr', String(254), unique=True)
    auth_code = Column('auth_code', String(8))
    expire_time = Column('expire_time', DateTime)

    def __init__(self, name: str, mailaddr: str, auth_code: str):
        times_to_expire = CONF.validation_timeout_in_sec
        self.name = name
        self.mailaddr = mailaddr
        self.auth_code = auth_code
        self.expire_time = datetime.fromtimestamp(int(time.time() + times_to_expire))

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
            "mailaddr='{}'".format(self.mailaddr),
            "auth_code='{}'".format(self.auth_code),
            "expire_time='{}'".format(self.expire_time),
        ])
        return "<CyUsersValidate({})".format(repr_args)


# class UsersExtraInfo(Base):
#     __tablename__ = 'users_extrainfo'
#     pass


class CyRecord(Base):
    __tablename__ = 'records'
    # __table_args__ = {
    #     'mysql_engine': 'InnoDB',
    #     'mysql_charset': 'utf8mb4',
    # }

    record_id = Column('record_id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(24), index=True, nullable=False)
    box_name = Column('box_name', String(32), nullable=False)
    last_update = Column('last_update', DateTime, onupdate=datetime.now)
    record_count = Column('record_count', Integer)
    record_data = Column('record_data', Binary(200))

    def __init__(self, name: str, box_name: str):
        self.name = name
        self.box_name = box_name
        self.last_update = datetime.now()
        self.record_count = 0
        self.record_data = b''

    def __repr__(self):
        repr_args = ', '.join([
            "record_id={}".format(self.record_id),
            "name='{}'".format(self.name),
            "box_name='{}'".format(self.box_name),
            "last_update='{}'".format(self.last_update),
            "record_count={}".format(self.record_count),
            "record_data=b'{}'".format(self.record_data),
        ])
        return "<CyRecord({})".format(repr_args)


class CyRecordArchive(Base):
    __tablename__ = 'records_archive'
    # __table_args__ = {'mysql_engine':'InnoDB'}

    record_id = Column('archive_id', Integer, primary_key=True)
    record_count = Column('record_count', Integer)
    record_data = Column('record_data', Binary(60000))

    def __init__(self, name: str, record_id: int):
        self.record_id = record_id
        self.record_count = 0
        self.record_data = b''

    def __repr__(self):
        repr_args = ', '.join([
            "name='{}'".format(self.name),
            "box_name='{}'".format(self.box_name),
            "record_data=b'{}'".format(self.record_data),
        ])
        return "<CyRecordArchive({})".format(repr_args)
