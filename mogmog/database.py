# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError

from mogmog.security import secure_hashing, mask_mailaddr

db = SQLAlchemy()

def setup_database(app: Flask):
    db.init_app(app)
    return db

class UserList(db.Model):
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


class UserMailaddr(db.Model):
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
