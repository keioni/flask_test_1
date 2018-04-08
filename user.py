# -*- coding: utf-8 -*-
"""
    Flask-Login user management module for my study program.

    by Kei Onimaru <otegami@devel.keys.jp>
"""

from flask_login import LoginManager
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username: str):
        self.username = username

    def get_id(self) -> str:
        return self.username


def authenticate(username: str, password: str) -> bool:
    if username == 'test' and password == 'test':
        return True
    else:
        return False
