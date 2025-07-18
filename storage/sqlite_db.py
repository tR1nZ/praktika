import sqlite3
from typing import List, Dict, Tuple
from storage.db_interface import DBInterface
from storage.models import BaseModel

class SQLiteDB(DBInterface):
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)

    def _execute_query(self, query: str, params: Tuple) -> List[Dict]:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def _replace_placeholders(self, query: str) -> str:
        return query.replace("%s", "?")

    def create(self, model: BaseModel) -> int:
        table = model.get_table_name()
        fields = model.to_dict()
        columns = ', '.join(fields.keys())
        placeholders = ', '.join(['?'] * len(fields))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(fields.values()))
        self.connection.commit()
        return cursor.lastrowid

    def insert_many(self, models: List[BaseModel]) -> List[int]:
        if not models:
            return []

        table = models[0].get_table_name()
        fields = models[0].to_dict().keys()
        columns = ', '.join(fields)
        placeholders = ', '.join(['?'] * len(fields))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        values = [tuple(model.to_dict().values()) for model in models]
        cursor.executemany(query, values)
        self.connection.commit()
        return [row[0] for row in cursor.execute("SELECT last_insert_rowid()").fetchall()]
