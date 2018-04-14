# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData
from sqlalchemy import String, Integer, DateTime

from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql://{user}:{passwd}@{host}/{db}'\
        .format(user=user, passwd=passwd, host=host, db=db_name),\
        encoding='utf-8', echo=False)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

metadata = MetaData(engine)
Base = declarative_base()

class UserList(Base):
    __tablename__ = 'userlist'
    __table_args__ = 