# -*- coding: utf-8 -*-


import os

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from orm.database import Session
from orm.database import (UserAuthTable, UserMailaddrTable,
                          UserValidationTable)
from orm.security import secure_hashing, generate_validation_code


def begin():
    return Session()

def end(session):
    session.close()

def get_user(name: str, session):
    return session.query(UserAuthTable).filter_by(name=name).first()

def auth(name: str, plain_password: str, salt: str, session) -> bool:
    password = secure_hashing(plain_password, salt)
    count = session.query(UserAuthTable).filter(
        and_(
            UserAuthTable.name == name,
            UserAuthTable.password == password
        )
    ).count()
    if count == 0:
        return False
    else:
        return True

def add(name: str, plain_password: str, mailaddr: str, salt: str, session) -> str:
    try:
        user_adding = UserAuthTable(name, plain_password, salt)
        session.add(user_adding)
        user_added = get_user(name, session)
        if user_adding == user_added:
            um = UserMailaddrTable(user_added.id, mailaddr, salt)
            session.add(um)
            validation_code = generate_validation_code()
            uv = UserValidationTable(user_added.id, mailaddr, salt, validation_code)
            session.add(uv)
    except IntegrityError:
        session.rollback()
        return ''
    except:
        session.rollback()
        raise
    session.commit()
    return validation_code

def get_validation_code(name: str, session) -> str:
    user = get_user(name, session)
    # user = session.query(UserAuthTable).filter_by(name=name).first()
    if user:
        user_id = int(user.id)
        uv = session.query(UserValidationTable).filter_by(id=user_id).first()
        if uv:
            return uv.validation_code
    return None

def validate(name: str, mailaddr: str, validation_code: str, salt: bytes, session) -> bool:
    user = get_user(name, session)
    # user = session.query(UserAuthTable).filter_by(name=name).first()
    if user:
        user_id = int(user.id)
        hashed_mailaddr = secure_hashing(mailaddr, salt)
        uv = session.query(UserValidationTable).filter(
            and_(UserValidationTable.id == user_id,
                 UserValidationTable.hashed_mailaddr == hashed_mailaddr,
                 UserValidationTable.validation_code == validation_code,
                )
        ).first()
        if uv:
            try:
                session.delete(uv)
                user = session.query(UserAuthTable).filter_by(id=user_id).first()
                user.status = 'Active'
                session.commit()
                return True
            except:
                session.rollback()
                raise
    return False

def delete(name: str, session) -> bool:
    user = get_user(name, session)
    # user = session.query(UserAuthTable).filter_by(name=name).first()
    if user:
        try:
            user_id = user.id
            session.delete(user)
            um = session.query(UserMailaddrTable).filter_by(id=user_id).first()
            if um:
                session.delete(um)
            uv = session.query(UserValidationTable).filter_by(id=user_id).first()
            if uv:
                session.delete(uv)
            session.commit()
            return True
        except:
            session.rollback()
            raise
    return False

class GnunuUserManager:

    def __init__(self, salt: str='', session=None):
        if salt == '':
            self.salt = os.environ.get('BLAKE2B_SALT', '').encode('utf-8')
        else:
            self.salt = salt.encode('utf-8')
        if session:
            self.session = session
        else:
            self.session = Session()

    def __del__(self):
        self.session.close()

    def close_session(self):
        self.session.close()

    def auth(self, name: str, plain_password: str) -> bool:
        return auth(name, plain_password, self.salt, self.session)

    def add(self, name: str, plain_password: str, mailaddr: str) -> str:
        return add(name, plain_password, mailaddr, self.salt, self.session)

    def validate(self, name: str, mailaddr: str, validation_code: str) -> bool:
        return validate(name, mailaddr, validation_code, self.salt, self.session)

    def delete(self, name: str) -> bool:
        return delete(name, self.session)
