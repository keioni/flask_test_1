# -*- coding: utf-8 -*-

import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from orm.security import secure_hashing, mask_mailaddr

engine = create_engine('sqlite:///userlist.sqlite3', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class UserList(Base):
    __tablename__ = 'user_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True)
    password = Column('password', String)
    mailaddr = Column('mailaddr', String, unique=True)
    registered_timestamp = Column('registered_timestamp', DateTime)

    def __init__(self, username: str, plain_password: str, plain_mailaddr: str):
        try:
            self.username = username
            self.password = secure_hashing(plain_password)
            self.mailaddr = secure_hashing(plain_mailaddr)
            self.registered_timestamp = datetime.utcnow()
        except IntegrityError:
            pass

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "username='{}'".format(self.username),
            "password='{}'".format(self.password),
            "mailaddr='{}'".format(self.mailaddr),
            "register_timestamp='{}'".format(self.registered_timestamp),
        ])
        return "<UserList({})".format(repr_args)


class UserMailaddr(Base):
    __tablename__ = 'user_mailaddr'

    id = Column('id', Integer, primary_key=True)
    mailaddr = Column('mailaddr', String, unique=True)
    masked_mailaddr = Column('masked_mailaddr', String)
    reset_code = Column('reset_code', String)
    resetting_date = Column('resetting_date', DateTime)

    def __init__(self, username: str, plain_mailaddr: str):
        self.masked_mailaddr = mask_mailaddr(plain_mailaddr)
        self.mailaddr = secure_hashing(plain_mailaddr)

    def __repr__(self):
        repr_args = ', '.join([
            "id={}".format((self.id)),
            "mailaddr='{}'".format(self.mailaddr),
            "masked_mailaddr='{}'".format(self.masked_mailaddr),
            "reset_code='{}'".format(self.reset_code),
            "resetting_date='{}'".format(self.resetting_date),
        ])
        return "<UserMailaddr({})".format(repr_args)
