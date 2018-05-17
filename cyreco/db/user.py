# -*- coding: utf-8 -*-

from typing import Union

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from cyreco.db import Session
from cyreco.db.model import CyUserAuth, CyUserProfile, CyUserValidate
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

    def get_user(self, name: str, session: Session):
        return session.query(CyUserAuth).filter_by(name=name).first()

    def auth(self, name: str, plain_password: str) -> bool:
        password = secure_hashing(plain_password, CONF.salt)
        session = Session()
        try:
            count = session.query(CyUserAuth).filter(
                and_(
                    CyUserAuth.name == name,
                    CyUserAuth.password == password
                )
            ).count()
            return bool(count)
        except:
            raise

    def add(self, name: str, plain_password: str, mailaddr: str) -> str:
        session = Session()
        try:
            session.add(CyUserAuth(
                name,
                plain_password,
                mailaddr,
            ))
            session.add(CyUserProfile(
                name,
            ))
            auth_code = generate_auth_code('digit', 6)
            session.add(CyUserValidate(
                name,
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
            uv = session.query(CyUserValidate).filter(
                and_(CyUserValidate.name == name,
                    CyUserValidate.mailaddr == mailaddr,
                    CyUserValidate.auth_code == auth_code,
                    )
            ).first()
            if uv:
                user = self.get_user(name, session)
                user.is_valid = True
                session.add(user)
                session.delete(uv)
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
            session.delete(user)
            um = session.query(CyUserProfile).filter_by(name=name).first()
            if um:
                session.delete(um)
            uv = session.query(CyUserValidate).filter_by(name=name).first()
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
