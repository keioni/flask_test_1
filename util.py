#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from hashlib import sha256
from base64 import b64encode

from orm.database import Base
from orm.user import GnunuUserManager

os.environ['BLAKE2B_SALT'] = 'oajokkN6AkwZB4wA0XpFtzlJpYYTVB7a9JkjV56PMAs='
user = GnunuUserManager()

args = sys.argv
if args[1] == 'create':
    Base.metadata.create_all()
elif args[1] == 'drop':
    Base.metadata.drop_all()
elif args[1] == 'add':
    vcode = user.add(args[2], args[3], args[4])  
    if vcode:
        print('user:{} added. [{}]'.format(args[2], vcode))
    else:
        print('FAILED: add_user({})'.format(args[2]))
elif args[1] == 'validate':
    if user.validate(args[2], args[3], args[4]):
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
elif args[1] == 'key':
    print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
