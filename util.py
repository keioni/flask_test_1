#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from cyreco.db import Base
from cyreco.db.user import CyrecoUserManager

user = CyrecoUserManager()

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
elif args[1] == 'auth':
    if user.auth(args[2], args[3]):
        print("user:{} authenticated.".format(args[2]))
    else:
        print("FAILED: auth_user({}).".format(args[2]))
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
elif args[1] == 'mail':
    from cyreco.utils.security import mask_mailaddr
    print('mailaddr: {}'.format(mask_mailaddr(args[2])))
# elif args[1] == 'query':
#     print(db.auth_user(args[2], args[3]))
# elif args[1] == 'key':
#     print(b64encode(sha256(os.urandom(24)).digest()).decode('utf-8'))
