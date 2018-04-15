# -*- coding: utf-8 -*-

import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Settings:

    def __init__(self, db_uri: str):
        self.database = db_uri
        self.engine = create_engine(db_uri, encoding = "utf-8", echo=True)
        self.metadata = MetaData(self.engine)
        self.salt = os.environ.get('BLAKE2B_SALT').encode('utf-8')


class UserList(Base):
    __tablename__ = 'user_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True)
    hashed_password = Column('hashed_password', String)
    registered_timestamp = Column('registered_timestamp', DateTime, default=datetime.utcnow)


class MailaddrList(Base):
    __tablename__ = 'user_mailaddr'

    id = Column('id', Integer, primary_key=True)
    masked_mailaddr = Column('masked_mailaddr', String)
    hashed_mailaddr = Column('hashed_mailaddr', String)
    reset_code = Column('reset_code', String)
    resetting_date = Column('resetting_date', DateTime)
