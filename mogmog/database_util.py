#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sqlalchemy import create_engine

from database import UserDatabase


args = sys.argv
engine = create_engine(UserDatabase.db_users)

if args[1] == 'c':
    UserDatabase.table_users.create(engine)
elif args[1] == 'd':
    UserDatabase.table_users.drop(engine)
elif args[1] == 'a':
    user = {
        'idx': int(args[2]),
        'username': args[3],
        'hashed_password': args[4],
    }
    print(user)
    db = UserDatabase()
    db.add_user(user)
