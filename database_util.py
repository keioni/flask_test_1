#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

args = sys.argv
argc = len(args)

engine = create_engine('sqlite:///users.sqlite3')

meta = MetaData()
user = Table('users', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('hashed_password', String, nullable=False),
)

if args[1] == 'c':
    user.create(engine)

elif args[1] == 'd':
    user.drop(engine)

