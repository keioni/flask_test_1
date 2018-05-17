# -*- coding: utf-8 -*-

from cyreco.db import Session
from cyreco.db.model import CyRecord, CyRecordArchive
from cyreco.utils.security import secure_hashing, generate_auth_code

from cyreco.sys.config import CONF


# class CyRecord:
#     pass


class CyRecordBox:
    name = ''
    records = []

    def __init__(self, name: str):
        self.name = name

    def add_record(self):
        pass


class CyRecordManager:

    def create_record_box(self, box_name: str):
        pass

    def destruct_record_box(self, box_name: str):
        pass

    def add_record(self, box_name: str):
        pass

    def delete_record(self, box_name: str):
        pass
