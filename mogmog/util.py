#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from hashlib import sha256
from base64 import b64decode, b64encode
from sqlalchemy import create_engine

from userlist import UserList

args = sys.argv
db = UserList('sqlite:///userlist.sqlite3')

if args[1] == 'c':
    db.userlist.create(db.engine)
elif args[1] == 'd':
    db.userlist.drop(db.engine)
elif args[1] == 'a':
    user = {
        'username': args[2],
        'hashed_password': args[3],
    }
    db.add_user(user)
    print('user:{} added.'.format(user['username']))
elif args[1] == 'key':
    print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
