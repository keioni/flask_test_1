# -*- coding: utf-8 -*-


import os
from typing import Union

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from orm.database import Session
from orm.database import UsersAuthData, UsersProfile, UsersValidation
from orm.security import secure_hashing, generate_auth_code

from cyreco.sys.config import conf


def auth_user(name: str, plain_password: str) -> bool:
    """
    Short cut for authenticating user purpose only.
    Session is opened and closed every calling.
    """

    user_man = GnunuUserManager()
    ret = user_man.auth(name, plain_password)
    user_man.close_session()
    return ret

class GnunuUserManager:
    """
    User Manager:
    Managing authenticating, adding, validating, and deleting user.

    'session' is expert option. If you still open session, use this option.
    """

    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = Session()
        self.auth_code = ''

    def __del__(self):
        self.session.close()

    def close_session(self):
        self.session.close()

    def get_user(self, key: Union[str, int]):
        if isinstance(key, str):
            return self.session.query(UsersAuthData). \
                    filter_by(name=key).first()
        elif isinstance(key, int):
            return self.session.query(UsersAuthData). \
                    filter_by(id=key).first()
        else:
            return

    def auth(self, name: str, plain_password: str) -> bool:
        password = secure_hashing(plain_password, conf.salt)
        count = self.session.query(UsersAuthData).filter(
            and_(
                UsersAuthData.name == name,
                UsersAuthData.password == password
            )
        ).count()
        if count == 0:
            return False
        else:
            return True

    def add(self, name: str, plain_password: str, mailaddr: str) -> str:
        try:
            user_adding = UsersAuthData(
                name,
                mailaddr,
                plain_password,
            )
            self.session.add(user_adding)
            user_added = self.get_user(name)
            if user_adding == user_added:
                self.session.add(UsersProfile(
                    user_added.id,
                ))
                auth_code = generate_auth_code('digit', 6)
                self.session.add(UsersValidation(
                    user_added.id,
                    mailaddr,
                    auth_code,
                ))
        except IntegrityError:
            self.session.rollback()
            return ''
        except:
            self.session.rollback()
            raise
        self.session.commit()
        return auth_code

    def validate(self, name: str, mailaddr: str, auth_code: str) -> bool:
        user = self.get_user(name)
        if not user:
            return False
        user_id = int(user.id)
        mailaddr = mailaddr
        uv = self.session.query(UsersValidation).filter(
            and_(UsersValidation.id == user_id,
                 UsersValidation.mailaddr == mailaddr,
                 UsersValidation.auth_code == auth_code,
                )
        ).first()
        if uv:
            try:
                self.session.delete(uv)
                user = self.get_user(user_id)
                user.valid = True
                self.session.commit()
                return True
            except:
                self.session.rollback()
                raise
        return False

    def delete(self, name: str) -> bool:
        user = self.get_user(name)
        if not user:
            return False
        try:
            user_id = user.id
            self.session.delete(user)
            um = self.session.query(UsersProfile). \
                    filter_by(id=user_id).first()
            if um:
                self.session.delete(um)
            uv = self.session.query(UsersValidation) \
                    .filter_by(id=user_id).first()
            if uv:
                self.session.delete(uv)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise
        return False
