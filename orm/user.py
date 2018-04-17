# -*- coding: utf-8 -*-

from hmac import compare_digest

from sqlalchemy import and_
from orm.database import UserList, UserMailaddr, Session
from orm.security import secure_hashing, mask_mailaddr


session = Session()

def auth_user(username: str, plain_password: str) -> int:
    password = secure_hashing(plain_password)
    return session.query(UserList).filter(
        and_(
            UserList.username == username,
            UserList.password == password
        )
    ).count()

def add_user(username: str, plain_password: str, plain_mailaddr: str) -> int:
    ul = UserList(username, plain_password, plain_mailaddr)
    count = session.add(ul)
    session.commit()
    if count > 0:
        um = UserMailaddr(username, plain_mailaddr)
        session.add(um)
        session.commit()
    return count

def delete_user(self, username: str) -> int:
    ul = session.query(UserList).filter_by(username=username).first()
    password = secure_hashing(ul.password)
    count = session.delete(ul)
    session.commit()
    if count > 0:
        um = session.query(UserMailaddr).filter_by(password=password).first()
        session.delete(um)
        session.commit()
    return count
