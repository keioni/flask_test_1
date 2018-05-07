# -*- coding: utf-8 -*-

from typing import Union

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from cyreco.db import Session
from cyreco.db.model import UsersAuthData, UsersProfile, UsersValidation
from cyreco.utils.security import secure_hashing, generate_auth_code

from cyreco.sys.config import CONF


def auth_user(name: str, plain_password: str) -> bool:
    """
    Short cut for authenticating user.
    This makes user manager and it's call auth method.
    """

    user_man = CyrecoUserManager()
    ret = user_man.auth(name, plain_password)
    return ret

class CyrecoUserManager:
    """
    User Manager:

    Managing authenticating, adding, validating, and deleting user.
    """

    def get_user(self, key: Union[str, int], session):
        if isinstance(key, str):
            return session.query(UsersAuthData).filter_by(name=key).first()
        elif isinstance(key, int):
            return session.query(UsersAuthData).filter_by(id=key).first()
        else:
            return

    def auth(self, name: str, plain_password: str) -> bool:
        password = secure_hashing(plain_password, CONF.salt)
        session = Session()
        try:
            count = session.query(UsersAuthData).filter(
                and_(
                    UsersAuthData.name == name,
                    UsersAuthData.password == password
                )
            ).count()
            if count == 0:
                return False
            else:
                return True
        except:
            raise

    def add(self, name: str, plain_password: str, mailaddr: str) -> str:
        session = Session()
        try:
            user_adding = UsersAuthData(
                name,
                plain_password,
                mailaddr,
            )
            session.add(user_adding)
            user_added = self.get_user(name, session)
            if user_adding == user_added:
                session.add(UsersProfile(
                    user_added.id,
                ))
                auth_code = generate_auth_code('digit', 6)
                session.add(UsersValidation(
                    user_added.id,
                    mailaddr,
                    auth_code,
                ))
        except IntegrityError:
            session.rollback()
            return ''
        except:
            session.rollback()
            raise
        session.commit()
        return auth_code

    def validate(self, name: str, mailaddr: str, auth_code: str) -> bool:
        session = Session()
        try:
            user = self.get_user(name, session)
            if not user:
                return False
            user_id = int(user.id)
            mailaddr = mailaddr
            uv = session.query(UsersValidation).filter(
                and_(UsersValidation.id == user_id,
                    UsersValidation.mailaddr == mailaddr,
                    UsersValidation.auth_code == auth_code,
                    )
            ).first()
            if uv:
                session.delete(uv)
                user = self.get_user(user_id, session)
                user.is_valid = True
                session.add(user)
        except:
            session.rollback()
            raise
        session.commit()
        return True

    def delete(self, name: str) -> bool:
        session = Session()
        try:
            user = self.get_user(name, session)
            if not user:
                return False
            user_id = user.id
            session.delete(user)
            um = session.query(UsersProfile).filter_by(id=user_id).first()
            if um:
                session.delete(um)
            uv = session.query(UsersValidation).filter_by(id=user_id).first()
            if uv:
                session.delete(uv)
        except:
            session.rollback()
            raise
        session.commit()
        return True

    def modify(self) -> bool:
        pass

    def activate_deactivate(self, name: str, flag: bool) -> bool:
        session = Session()
        try:
            user = self.get_user(name, session)
            if not user:
                return False
            user.is_active = flag
            session.add(user)
        except:
            session.rollback()
            raise
        session.commit()
        return True
