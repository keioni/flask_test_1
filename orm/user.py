# -*- coding: utf-8 -*-

from orm.database import UserList, UserMailaddr, db
from orm.security import secure_hashing, mask_mailaddr

def auth_user(username: str, raw_password: str) -> bool:
    password = secure_hashing(raw_password)
    return True
    # stmt = self.userlist.select().where(
    #     and_(
    #         self.userlist.c.username == username,
    #         self.userlist.c.hashed_password == hashed_password
    #     )
    # )
    # with self.engine.connect() as conn:
    #     result = conn.execute(stmt)
    #     if result.fetchone():
    #         return True
    # return False

def add_user(username: str, raw_password: str, raw_mailaddr: str) -> bool:
    user = UserList(username, raw_password, raw_mailaddr)
    db.session. add(user)
    # stmt = self.userlist.insert().values( # pylint: disable=E1120
    #     username=username,
    #     hashed_password=hashed_password,
    # )
    # with self.engine.connect() as conn:
    #     try:
    #         if conn.execute(stmt).rowcount:
    #             return True
    #     except IntegrityError:
    #         return False
    # return False
    return True

def delete_user(self, username: str) -> bool:
    # stmt = self.userlist.delete().where( # pylint: disable=E1120
    #     self.userlist.c.username == username
    # )
    # with self.engine.connect() as conn:
    #     if conn.execute(stmt).rowcount:
    #         return True
    # return False
    return True
