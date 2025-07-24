from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
from storage.base_model import BaseModel

class DBInterface(ABC):
    @abstractmethod
    def _execute_query(self, query: str, params: Tuple = ()) -> Any:
        """Выполняет одиночный SQL-запрос."""
        pass


    def get_create_query(self, models: List[BaseModel]) -> str:
        if not models:
            return []

        table = models[0].get_table_name()
        columns = models[0].get_column_types()

        column_defs = [f"{name} {sql_type}" for name, sql_type in columns.items()]
        # здесь можно добавить FK если нужно — например:
        # if name.endswith("_id"): column_defs.append(f"FOREIGN KEY({name}) REFERENCES ...")

        column_sql = ', '.join(column_defs)
        return f"CREATE TABLE IF NOT EXISTS {table} ({column_sql})"

    def insert_many(self, models: List[BaseModel]) -> List[int]:
        if not models:
            return []

        table = models[0].get_table_name()
        keys = models[0].to_dict().keys()
        columns = ', '.join(keys)
        placeholders = ', '.join(['?'] * len(keys))

        values_list = [tuple(model.to_dict().values()) for model in models]
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        self._executemany(query, values_list)

        return self._last_insert_ids(len(values_list))
    

    def python_type_to_sql(py_type: type) -> str:
        """Преобразование Python-типа в SQL-тип."""
        if py_type == int:
            return "INTEGER"
        elif py_type == float:
            return "REAL"
        elif py_type == str:
            return "TEXT"
        elif py_type == bool:
            return "INTEGER"
        elif py_type in (dict, list):
            return "TEXT"
        else:
            return "TEXT"  # по умолчанию сериализуем
        
        
