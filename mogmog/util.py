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

if args[1] == 'create':
    db.userlist.create(db.engine)
elif args[1] == 'drop':
    db.userlist.drop(db.engine)
elif args[1] == 'add':
    if db.add_user(args[2], args[3]):
        print('user:{} added.'.format(args[2]))
    else:
        print('FAILED: add_user({})'.format(args[2]))
elif args[1] == 'delete':
    if db.delete_user(args[2]):
        print('user:{} deleted.'.format(args[2]))
    else:
        print('FAILED: delete_user({})'.format(args[2]))
elif args[1] == 'query':
    print(db.auth_user(args[2], args[3]))
elif args[1] == 'key':
    print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
