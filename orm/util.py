#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from hashlib import sha256
from base64 import b64decode, b64encode
from sqlalchemy import create_engine

from orm.security import salt
from orm.database import Base
import orm.user as user

salt = "oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs=".encode('utf-8')
args = sys.argv

if args[1] == 'create':
    Base.metadata.create_all()
elif args[1] == 'drop':
    Base.metadata.drop_all()
elif args[1] == 'add':
    if user.add(args[2], args[3], args[4]):
        print('user:{} added.'.format(args[2]))
    else:
        print('FAILED: add_user({})'.format(args[2]))
elif args[1] == 'validate':
    if len(args) > 4:
        vcode = args[4]
    else:
        vcode = user.get_validation_code(args[2])
        print("user:{}, vcode:{}".format(args[2], vcode))
    if user.validate(args[2], args[3], vcode):
        print("user:{} validated.".format(args[2]))
    else:
        print('FAILED: validate_user({})'.format(args[2]))
elif args[1] == 'delete':
    if user.delete(args[2]):
        print('user:{} deleted.'.format(args[2]))
    else:
        print('FAILED: delete_user({})'.format(args[2]))
# elif args[1] == 'query':
#     print(db.auth_user(args[2], args[3]))
# elif args[1] == 'key':
#     print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
