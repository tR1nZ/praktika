from storage.base_model import BaseModel
import json
from typing import Dict, Any
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt

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






class Strobe(BaseModel):
    _values: npt.NDArray #нельзя хранить в бд
    # _values:dict #нельзя хранить в бд
    path:str
    length:int

class Verifstamp(BaseModel):
    kgd: int
    kgrs: int
    value: float

    # @classmethod
    # def from_dict(cls, data: Dict[str, Any]):
    #     return cls(**data)

class Verif(BaseModel):
    # valid: int  # bool в виде int (0/1)
    verif: npt.NDArray
    # src_verif: npt.NDArray
    # ftps: Strobe

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            verif=np.NDArray([
                [Verifstamp.from_dict(item) for item in group]
                for group in data.get("src_verif", [])
            ]),
        )
    
    def to_dict():
        pass


"""
class Input(BaseModel):
    verif: Verif
    verif_seq: Strobe[complex_double] #ftps
    data: Strobe[complex_int64]
    param: Param
    mseq: Strobe[npt.int8]
    test_name: str

class Output(BaseModel):
    verif: Verif
    data: Strobe[complex_double]
    time: Time
"""
class Data(BaseModel):
    param_id: int
    time_id: int
    verif_id: int
    strobe_id: int
    output_id: int
    polar: int
    path: str

class InputDB(BaseModel):
    id: int
    param_id: int # FK
    verif_id: int
    verif_seq_id: int
    input_data_id: int
    mseq_id: int
    path: str

class OutputDB(BaseModel):
    id: int
    verif_id: int
    output_data_id: int
    time_id: int
    input_id: int
