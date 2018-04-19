# -*- coding: utf-8 -*-

from hmac import compare_digest

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from database import Session
from database import UserAuthTable, UserMailaddrTable, \
                         UserValidationTable
from security import secure_hashing, mask_mailaddr


session = Session()

def auth(name: str, plain_password: str) -> int:
    password = secure_hashing(plain_password)
    return session.query(UserAuthTable).filter(
        and_(
            UserAuthTable.name == name,
            UserAuthTable.password == password
        )
    ).count()

def add(name: str, plain_password: str, mailaddr: str) -> int:
    try:
        uat = UserAuthTable(name, plain_password)
        count = uat.scalar()
        session.add(uat)
        if count > 0:
            id = session.query(UserAuthTable.id).filter_by(name=name).first()
            session.begin()
            umt = UserMailaddrTable(id, mailaddr)
            session.add(umt)
            uvt = UserValidationTable(id, mailaddr)
            session.add(uvt)
    except IntegrityError:
        session.rollback()
    finally:
            session.commit()
    return count

def validate(name: str, mailaddr: str, validation_code: str) -> int:
    hashed_mailaddr = secure_hashing(mailaddr)
    id = session.query(UserAuthTable.id).filter_by(name=name).first()
    uvt = session.query(UserValidationTable).filter(
        and_(UserValidationTable.id == id,
            UserValidationTable.hashed_mailaddr == hashed_mailaddr,
            UserValidationTable.validation_code == validation_code,
        )
    ).first()
    count = uvt.scalar()
    if count > 0:
        session.delete(uvt)
        uat = session.query(UserAuthTable).filter_by(id=id).first()
        uat.status = 'Active'
        session.commit()
    return count

def delete(name: str) -> int:
    uat = session.query(UserAuthTable).filter_by(name=name).first()
    id = uat.id
    count = uat.scalar()
    if count > 0:
        session.delete(uat)
        umt = session.query(UserMailaddrTable).filter_by(id=id).first()
        count = umt.scalar()
        if count > 0:
            session.delete(umt)
    session.commit()
    return count
