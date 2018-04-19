# -*- coding: utf-8 -*-


from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from orm.database import Session
from orm.database import (UserAuthTable, UserMailaddrTable,
                      UserValidationTable)
from orm.security import secure_hashing


session = Session()

def auth(name: str, plain_password: str) -> int:
    password = secure_hashing(plain_password)
    return session.query(UserAuthTable).filter(
        and_(
            UserAuthTable.name == name,
            UserAuthTable.password == password
        )
    ).count()

def add(name: str, plain_password: str, mailaddr: str) -> bool:
    try:
        user_adding = UserAuthTable(name, plain_password)
        session.add(user_adding)
        user_added = session.query(UserAuthTable).filter_by(name=name).first()
        if user_adding == user_added:
            um = UserMailaddrTable(user_added.id, mailaddr)
            session.add(um)
            uv = UserValidationTable(user_added.id, mailaddr)
            session.add(uv)
    except IntegrityError:
        session.rollback()
        return False
    except:
        session.rollback()
        raise
    session.commit()
    return True

def get_validation_code(name: str) -> str:
    user = session.query(UserAuthTable).filter_by(name=name).first()
    if user:
        user_id = int(user.id)
        uv = session.query(UserValidationTable).filter_by(id=user_id).first()
        if uv:
            return uv.validation_code
    return None
 
def validate(name: str, mailaddr: str, validation_code: str) -> bool:
    user = session.query(UserAuthTable).filter_by(name=name).first()
    if user:
        user_id = int(user.id)
        hashed_mailaddr = secure_hashing(mailaddr)
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

def delete(name: str) -> bool:
    user = session.query(UserAuthTable).filter_by(name=name).first()
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
