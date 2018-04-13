#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from hashlib import sha256
from base64 import b64decode, b64encode
from sqlalchemy import create_engine

from userlist import UserList

args = sys.argv
os.environ['BLAKE2B_SALT'] = "oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs="
db = UserList('sqlite:///userlist.sqlite3')

if args[1] == 'c':
    db.userlist.create(db.engine)
elif args[1] == 'd':
    db.userlist.drop(db.engine)
elif args[1] == 'a':
    db.add_user(args[2], args[3])
    print('user:{} added.'.format(args[2]))
elif args[1] == 'q':
    # db.query_userdata(args[2])
    query = db.userlist.select().where(db.userlist.c.username == ':username')
    print(query)
    conn = db.engine.connect()
    result = conn.execute(query)
    for row in result:
        print(row)
    else:
        print("Oh...")
elif args[1] == 'key':
    print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
