# -*- coding: utf-8 -*-

import os
import string
import time
from datetime import datetime
from random import choice

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from security import secure_hashing, mask_mailaddr

engine = create_engine('sqlite:///userlist.sqlite3', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class UserAuthTable(Base):
    __tablename__ = 'user_auth'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user = Column('user', String, unique=True)
    password = Column('password', String)
    status = Column('status', String)
    ctime = Column('ctime', Integer)
    mtime = Column('mtime', Integer)

    def __init__(self, user: str, plain_password: str):
        self.user = user
        self.password = secure_hashing(plain_password)
        self.status = ''
        self.ctime = self.mtime = int(time.time())

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "user='{}'".format(self.user),
            "password='{}'".format(self.password),
            "status='{}'".format(self.status),
            "ctime={}".format(self.ctime),
            "mtime={}".format(self.mtime),
        ])
        return "<UserAuthTable({})".format(repr_args)


class UserMailaddrTable(Base):
    __tablename__ = 'user_mailaddr'

    id = Column('id', Integer, primary_key=True)
    hashed_mailaddr = Column('hashed_mailaddr', String, unique=True)
    masked_mailaddr = Column('masked_mailaddr', String)
    # reset_code = Column('reset_code', String)
    # resetting_date = Column('resetting_date', DateTime)

    def __init__(self, id: int, mailaddr: str):
        self.id = id
        self.hashed_mailaddr = secure_hashing(mailaddr)
        self.masked_mailaddr = mask_mailaddr(mailaddr)

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "hashed_mailaddr='{}'".format(self.hashed_mailaddr),
            "masked_mailaddr='{}'".format(self.masked_mailaddr),
            # "reset_code='{}'".format(self.reset_code),
            # "resetting_date='{}'".format(self.resetting_date),
        ])
        return "<UserMailaddrTable({})".format(repr_args)


class UserValidationTable(Base):
    __tablename__ = 'user_gvalidation'

    id = Column('id', Integer, primary_key=True)
    hashed_mailaddr = Column('hashed_mailaddr', String, unique=True)
    validation_code = Column('validation_code', String)
    expire_time = Column('expire_time', Integer)

    def __init__(self, id: int, mailaddr: str):
        self.id = id
        self.hashed_mailaddr = secure_hashing(mailaddr)
        alphabet = string.ascii_letters + string.digits
        self.validation_code = ''.join(choice(alphabet) for i in range(8))
        self.expire_time = int(time.time()) + 3600

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format(self.id),
            "hashed_mailaddr='{}'".format(self.hashed_mailaddr),
            "validation_code='{}'".format(self.validation_code),
            "expire_time={}".format(self.expire_time),
        ])
        return "<UserRegisterValidationTable({})".format(repr_args)

#Base.metadata.create_all(engine)
