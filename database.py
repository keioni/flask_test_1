# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)

    def __repl__(self):
        ret = "<User(username='{}', hashed_password='{}')>".format(
            self.username,
            self.hashed_password,
        )
        return ret
