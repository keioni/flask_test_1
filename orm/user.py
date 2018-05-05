# -*- coding: utf-8 -*-


import os
from typing import Union

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from orm.database import Session
from orm.database import (UsersAuthData, UsersProfile,
                          UserValidationTable)
from orm.security import secure_hashing, generate_validation_code


def auth_user(name: str, plain_password: str, salt: str='') -> bool:
    """
    Short cut for authenticating user purpose only.
    When 'salt' is not specified, get form OS environment valiable.
    Session is opened and closed every calling.
    """

    user_man = GnunuUserManager(salt)
    ret = user_man.auth(name, plain_password)
    user_man.close_session()
    return ret

class GnunuUserManager:
    """
    User Manager:
    Managing authenticating, adding, validating, and deleting user.

    If 'salt' is not set, obtain from OS environment variable.
    'session' is expert option. If you still open session, use this option.
    """

    def __init__(self, salt: str='', session=None):
        if salt == '':
            salt = os.environ.get('BLAKE2B_SALT')
        self.salt = salt.encode('utf-8')
        if session:
            self.session = session
        else:
            self.session = Session()
        self.validation_code = ''

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
        password = secure_hashing(plain_password, self.salt)
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
            user_adding = UsersAuthData(name, mailaddr, plain_password)
            self.session.add(user_adding)
            user_added = self.get_user(name)
            if user_adding == user_added:
                self.session.add(UsersProfile(
                    user_added.id,
                ))
                validation_code = generate_validation_code()
                self.session.add(UserValidationTable(
                    user_added.id,
                    mailaddr,
                    self.salt,
                    validation_code
                ))
        except IntegrityError:
            self.session.rollback()
            return ''
        except:
            self.session.rollback()
            raise
        self.session.commit()
        return validation_code

    def validate(self, name: str, mailaddr: str, validation_code: str) -> bool:
        user = self.get_user(name)
        if not user:
            return False
        user_id = int(user.id)
        hashed_mailaddr = secure_hashing(mailaddr, self.salt)
        uv = self.session.query(UserValidationTable).filter(
            and_(UserValidationTable.id == user_id,
                 UserValidationTable.hashed_mailaddr == hashed_mailaddr,
                 UserValidationTable.validation_code == validation_code,
                )
        ).first()
        if uv:
            try:
                self.session.delete(uv)
                user = self.get_user(user_id)
                user.status = 'Active'
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
            uv = self.session.query(UserValidationTable) \
                    .filter_by(id=user_id).first()
            if uv:
                self.session.delete(uv)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise
        return False
