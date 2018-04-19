# -*- coding: utf-8 -*-

import os
import re
from hashlib import blake2b # pylint: disable=E0611
from hmac import compare_digest
from base64 import b64decode, b64encode

salt: str = ''
pat_mailaddr = re.compile(r'^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\.\-]+$')

def secure_hashing(value: str) -> str:
    h = blake2b(key=salt, digest_size=32)
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()

def mask_mailaddr(mailaddr: str) -> str:
    match = pat_mailaddr.search()
    if match:
        user = match.group(0)
        domain = match.group(1)
    return user + domain

