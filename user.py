#!/usr/bin/env python
# coding: utf-8

from flask_login import LoginManager
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username: str):
        self.username = username
        self.password: str = ''

    # def is_authenticated(self) -> bool:
    #     return True

    # def is_active(self) -> bool:
    #     return True
    
    def get_id(self) -> str:
        return self.username


def authenticate(username: str, password: str) -> bool:
    if username == 'test' and password == 'test':
        return True
    else:
        return False
