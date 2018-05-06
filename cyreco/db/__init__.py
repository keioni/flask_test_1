# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from cyreco.sys.config import CONF

engine = create_engine(CONF.db_connect_string, echo=CONF.debug_sql_print)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
