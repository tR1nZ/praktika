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




class Verifstamp(BaseModel):
    kgd: int
    kgrs: int
    value: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)


class Verif(BaseModel):
    valid: int  # bool в виде int (0/1)
    out_verif: list(list(Verifstamp))
    src_verif: list(list(Verifstamp))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            valid=data["is_data_valid"],
            out_verif=[
                [Verifstamp.from_dict(item) for item in group]
                for group in data.get("out_verif", [])
            ],
            src_verif=[
                [Verifstamp.from_dict(item) for item in group]
                for group in data.get("src_verif", [])
            ],
        )




class Strobe(BaseModel):
    _values:dict #нельзя хранить в бд
    path:str
    length:int



class Output(BaseModel):
    out_arr: list
    out_verif: list





class Data(BaseModel):
    param_id: int
    time_id: int
    verif_id: int
    strobe_id: int
    output_id: int
    polar: int
    path: str


