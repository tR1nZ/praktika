from base_model import BaseModel
import json
from typing import Dict, Any


class Param(BaseModel):
    def __init__(self, distr, is_am, kgd, kgrs, n1grs, ndec, nfgd_fu, nl, samples_num, shgd, true_nins):
        self.distr = distr
        self.is_am = is_am
        self.kgd = kgd
        self.kgrs = kgrs
        self.n1grs = n1grs
        self.ndec = ndec
        self.nfgd_fu = nfgd_fu
        self.nl = nl
        self.samples_num = samples_num
        self.shgd = shgd
        self.true_nins = true_nins

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_db_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Param":
        return cls(**data)

    @classmethod
    def get_table_name(cls) -> str:
        return "param"


class Time(BaseModel):
    def __init__(self, cpu_test, date, fft, read_data, sine, time, total, write):
        self.cpu_test = cpu_test
        self.date = date
        self.fft = fft
        self.read_data = read_data
        self.sine = sine
        self.time = time
        self.total = total
        self.write = write

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_db_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Time":
        return cls(**data)

    @classmethod
    def get_table_name(cls) -> str:
        return "time"


class Verif(BaseModel):
    def __init__(self, valid, out_verif, src, verif_data):
        self.valid = valid
        self.out_verif = out_verif
        self.src = src
        self.verif_data = verif_data

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_db_dict(self) -> Dict[str, Any]:
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

    def to_db_dict(self) -> Dict[str, Any]:
        return {"values": json.dumps(self.values)}

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

    def to_db_dict(self) -> Dict[str, Any]:
        return {"out_arr": json.dumps(self.out_arr), "out_verif": self.out_verif}

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

    def to_db_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Data":
        return cls(**data)

    @classmethod
    def get_table_name(cls) -> str:
        return "data"
