# -*- coding: utf-8 -*-

import re
import string
from random import choice
from hashlib import blake2b # pylint: disable=E0611
from base64 import b64encode


PAT_MAILADDR = r'^([a-zA-Z0-9_\.\-]+)@([a-zA-Z0-9_\.\-]+)$'

def generate_validation_code(number_of_digits: int=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(choice(alphabet) for i in range(number_of_digits))

def secure_hashing(value: str, salt: bytes) -> str:
    h = blake2b(key=salt, digest_size=32)
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()

def mask_mailaddr(mailaddr: str) -> str:
    match = re.search(PAT_MAILADDR, mailaddr)
    if match:
        user = match.group(1)
        domain = match.group(2)
    return user + domain
