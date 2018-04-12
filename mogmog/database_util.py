#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sqlalchemy import create_engine

from userlist import UserList


args = sys.argv
engine = create_engine(UserList.db_userlist)

if args[1] == 'c':
    UserList.userlist.create(engine)
elif args[1] == 'd':
    UserList.userlist.drop(engine)
elif args[1] == 'a':
    user = {
        'idx': int(args[2]),
        'username': args[3],
        'hashed_password': args[4],
    }
    db = UserList()
    db.add_user(user)
