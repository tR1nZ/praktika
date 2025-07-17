from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        pass

    @abstractmethod
    def to_db_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def get_table_name(cls) -> str:
        pass

class Param(BaseModel):
    def __init__(self, dlstr: str, is_am: bool, kgd: int):
        self.dlstr = dlstr
        self.is_am = is_am
        self.kgd = kgd

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dlstr": self.dlstr,
            "is_am": self.is_am,
            "kgd": self.kgd
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Param":
        return cls(
            dlstr=data["dlstr"],
            is_am=data["is_am"],
            kgd=data["kgd"]
        )

    def to_db_dict(self) -> Dict[str, Any]:
        return self.to_dict()

    @classmethod
    def get_table_name(cls) -> str:
        return "params"
