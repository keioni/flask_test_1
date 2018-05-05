# -*- coding: utf-8 -*-

import time

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from orm.security import secure_hashing, generate_validation_code


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

    def __init__(self, name: str, mailaddr: str, plain_password: str, salt: str):
        self.name = name
        self.mailaddr = mailaddr
        self.password = secure_hashing(plain_password, salt)
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


class UserValidationTable(Base):
    __tablename__ = 'user_gvalidation'

    id = Column('id', Integer, primary_key=True)
    hashed_mailaddr = Column('hashed_mailaddr', String, unique=True)
    validation_code = Column('validation_code', String)
    expire_time = Column('expire_time', Integer)

    def __init__(self, user_id: int, mailaddr: str, salt: str, validation_code: str=''):
        self.id = user_id
        self.hashed_mailaddr = secure_hashing(mailaddr, salt)
        self.validation_code = ''
        if validation_code != '':
            self.validation_code = validation_code
        else:
            if self.validation_code != '':
                self.validation_code = generate_validation_code()
        self.expire_time = int(time.time()) + 3600

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format(self.id),
            "hashed_mailaddr='{}'".format(self.hashed_mailaddr),
            "validation_code='{}'".format(self.validation_code),
            "expire_time={}".format(self.expire_time),
        ])
        return "<UserRegisterValidationTable({})".format(repr_args)


class UsersExtraInfo(Base):
    __tablename__ = 'users_extrainfo'
    pass


class UsersRecord(Base):
    __tablename__ = 'users_record'
    pass
