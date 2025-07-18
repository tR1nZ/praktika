import json
from typing import List, Type, TypeVar
from storage.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class JSONLoader:
    @staticmethod
    def load_from_file(file_path: str, model_class: Type[T]) -> T:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return model_class.from_dict(data)
