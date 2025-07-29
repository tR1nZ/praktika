from storage.base_model import BaseModel
import json
from typing import Dict, Any
from dataclasses import dataclass



@dataclass
class Param(BaseModel):
    nl: int
    true_nihs: int
    samples_num: int
    kgd: int
    nfgd_fu: int
    shgd: int
    kgrs: int
    n1grs: int
    dlstr: int
    ndec: int
    is_am: int # bool


class Timestamp(BaseModel):
    duration:float
    end:float
    start:float


class Time(BaseModel):

    date: str
    time: str
    
    # Временные интервалы как объекты Timestamp
    cpu_testing_time: Timestamp
    fft: Timestamp
    read_data: Timestamp
    sine: Timestamp
    total: Timestamp
    write_data: Timestamp

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # Основные поля
        result = {
            'date': data['date'],
            'time': data['time']
        }
        
        # Автоматически создаем Timestamp объекты
        for key, value in data.items():
            if key not in ['date', 'time'] and isinstance(value, dict):
                result[key] = Timestamp.from_dict(value)
        
        return cls(**result)





class Verif(BaseModel):
    def __init__(self, valid, out_verif, src, verif_data):
        self.valid = valid
        self.out_verif = out_verif
        self.src = src
        self.verif_data = verif_data

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Verif":
        return cls(**data)

    @classmethod
    def get_table_name(cls) -> str:
        return "verif"


class Strobe(BaseModel):
    def __init__(self, values):
        self.values = values

    def to_dict(self) -> Dict[str, Any]:
        return {"values": self.values}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Strobe":
        return cls(data["values"])

    @classmethod
    def get_table_name(cls) -> str:
        return "strobe"


class Output(BaseModel):
    def __init__(self, out_arr, out_verif):
        self.out_arr = out_arr
        self.out_verif = out_verif

    def to_dict(self) -> Dict[str, Any]:
        return {"out_arr": self.out_arr, "out_verif": self.out_verif}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Output":
        return cls(data["out_arr"], data["out_verif"])

    @classmethod
    def get_table_name(cls) -> str:
        return "output"


class Data(BaseModel):
    def __init__(self, param_id, time_id, verif_id, strobe_id, output_id, polar, path):
        self.param_id = param_id
        self.time_id = time_id
        self.verif_id = verif_id
        self.strobe_id = strobe_id
        self.output_id = output_id
        self.polar = polar
        self.path = path

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Data":
        return cls(**data)

    @classmethod
    def get_table_name(cls) -> str:
        return "data"
