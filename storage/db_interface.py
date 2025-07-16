from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from base_model import BaseModel

class DBInterface(ABC):
    @abstractmethod
    def _execute_query(self, query: str, params: Tuple) -> List[Dict]:
        pass

    @abstractmethod
    def create(self, model: BaseModel) -> int:
        pass

    @abstractmethod
    def insert_many(self, models: List[BaseModel]) -> List[int]:
        pass
