# -*- coding: utf-8 -*-

import string
from random import choice
from hashlib import blake2b # pylint: disable=E0611
from base64 import b64encode

UNVAILED_DOMAINS = (
    'yahoo.co.jp',
    'gmail.com',
    'excite.co.jp',
    'outlook.jp',
    'outlook.com',
    'hotmail.co.jp',
    'live.jp',
    'zoho.com',
    'docomo.ne.jp',
    'ezweb.ne.jp',
    'au.com',
    'softbank.ne.jp',
)

def generate_auth_code(gen_type: str, number_of_digits: int):
    p = ''
    if 'upper' in gen_type:
        p = p + string.ascii_uppercase
    if 'lower' in gen_type:
        p = p + string.ascii_lowercase
    if 'digit' in gen_type:
        p = p + string.digits
    return ''.join(choice(p) for i in range(number_of_digits))

def secure_hashing(value: str, salt: str) -> str:
    salt = salt.encode('utf-8')
    h = blake2b(key=salt, digest_size=32)
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()

def mask_mailaddr(mailaddr: str) -> str:
    user, domain = mailaddr.split('@')
    len_user = len(user)
    if len_user == 1:
        user = '*'
    if len_user < 5:
        user = user[:1] + ('*' * (len_user - 1))
    if len_user < 9:
        user = user[:2] + ('*' * (len_user - 2))
    else:
        user = user[:2] + ('*' * (len_user - 3)) + user[-1]
    if domain not in UNVAILED_DOMAINS:
        len_domain = len(domain)
        if len_domain < 8:
            domain = '*' + domain[1:]
        elif len_domain < 12:
            domain = '**' + domain[2:]
        else:
            domain = '***' + domain[3:]
    return user + '@' + domain
