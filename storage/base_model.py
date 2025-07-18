from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)
    
    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

