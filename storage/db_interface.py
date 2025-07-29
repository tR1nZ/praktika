from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
from storage.base_model import BaseModel

class DBInterface(ABC):

    def _python_type_to_sql(self, py_type: type) -> str:
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
            return "TEXT"  

    def _get_column_types(self, models: BaseModel) -> Dict[str, str]:
        result = {}
        for key, value in models.to_dict().items():
            result[key] = self._python_type_to_sql(type(value))
        return result

    def _execute_query(self, query: str, params: Tuple = ()) -> Any:
        """Выполняет одиночный SQL-запрос."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


    def create(self, models: List[BaseModel]) -> str:
        if not models:
            return []

        table = models[0].get_table_name()
        columns = self._get_column_types(models[0])

        column_defs = [f"{name} {sql_type}" for name, sql_type in columns.items()]
        # здесь можно добавить FK если нужно — например:
        # if name.endswith("_id"): column_defs.append(f"FOREIGN KEY({name}) REFERENCES ...")

        column_sql = ', '.join(column_defs)
        query =  f"CREATE TABLE IF NOT EXISTS {table} ({column_sql})"
        self._execute_query(query)

    def insert_many(self, models: List[BaseModel]) -> List[int]:
        if not models:
            return []

        # Get table name and column keys from the first model
        table = models[0].get_table_name()
        keys = list(models[0].to_dict().keys())  # Ensure keys are in a consistent order
        columns = ', '.join(keys)
        num_columns = len(keys)
        
        # Create a placeholder for a single row: "(?, ?, ...)"
        row_placeholder = f"({', '.join(['?'] * num_columns)})"
        # Create placeholders for all rows: "(?, ?, ...), (?, ?, ...), ..."
        all_placeholders = ', '.join([row_placeholder] * len(models))
        
        # Flatten all values from all models in order of the keys
        values = []
        for model in models:
            model_dict = model.to_dict()
            # Ensure values are in the same order as 'keys'
            values.extend(model_dict[key] for key in keys)
        
        query = f"INSERT INTO {table} ({columns}) VALUES {all_placeholders}"
        self._execute_query(query, values)
        # Return the last inserted row IDs (implementation-specific)
        #return self.cursor.lastrowid






        
        
