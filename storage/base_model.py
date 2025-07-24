from abc import ABC, abstractmethod
from typing import Dict, Any


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


class BaseModel(ABC):
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)
    
    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__.lower()

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_column_types(self) -> Dict[str, str]:
        """Автоматически определяет SQL-типы для всех полей."""
        result = {}
        for key, value in self.to_dict().items():
            result[key] = python_type_to_sql(type(value))
        return result
     
    @abstractmethod 
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