import sqlite3
from typing import List, Dict, Tuple
from storage.db_interface import DBInterface
from storage.models import BaseModel



class SQLiteDB(DBInterface):
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        #добавить плейсхолдеры и курсор

