from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
from storage.base_model import BaseModel

class DBInterface(ABC):
    @abstractmethod
    def _execute_query(self, query: str, params: Tuple = ()) -> Any:
        """Выполняет одиночный SQL-запрос."""
        pass

    def create(self, model: BaseModel) -> int:
        table = model.get_table_name()
        data = model.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self._execute_query(query, values)

        return self._last_insert_id()

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
