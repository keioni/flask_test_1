# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Settings:

    def __init__(self, db_uri: str):
        self.database = db_uri
        self.engine = create_engine(DATABASE, encoding = "utf-8", echo=True)
        self.metadata = MetaData(self.engine)
        self.salt = os.environ.get('BLAKE2B_SALT').encode('utf-8')


class UserList(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    registered_timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password
        self.registered_timestamp = tim