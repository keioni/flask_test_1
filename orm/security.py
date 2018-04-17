# -*- coding: utf-8 -*-

import os
from hashlib import blake2b # pylint: disable=E0611
from hmac import compare_digest
from base64 import b64decode, b64encode

salt = os.environ.get('BLAKE2B_SALT').encode('utf-8')

def secure_hashing(value: str) -> str:
    h = blake2b(key=salt, digest_size=32)
    h.update(value.encode('utf-8'))
    return b64encode(h.digest()).decode()

def mask_mailaddr(mailaddr: str) -> str:
    return mailaddr

