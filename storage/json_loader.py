import json
from typing import List, Type, TypeVar
from storage.base_model import BaseModel
from storage.models import *
import re
import numpy as np

T = TypeVar('T', bound=BaseModel)

class JSONLoader:
    @staticmethod
    def load_from_file(file_path: str, model_class: Type[T]) -> T:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return model_class.from_dict(data)

    @staticmethod
    def parse_complex_array(v: List[List[float]]) -> np.ndarray:
        return np.array([complex(re_, im_) for re_, im_ in v], dtype=complex)

    @staticmethod
    def build_ndarray_dynamic(data):
        arr = np.empty((0,0,0), dtype=complex)

        for key, v in data.items():
            n, m = map(int, re.findall(r'\d+', key))
            print(n, m)
            vec = JSONLoader.parse_complex_array(v)
            K = vec.shape[0]

            # вычисляем новую форму, если нужно расширить
            new_M = max(arr.shape[0], m+1)
            new_N = max(arr.shape[1], n+1)
            new_K = max(arr.shape[2], K)

            if (new_M, new_N, new_K) != arr.shape:
                padded = np.zeros((new_M, new_N, new_K), dtype=complex)
                padded[:arr.shape[0], :arr.shape[1], :arr.shape[2]] = arr
                arr = padded

            arr[m, n, :K] = vec

        return arr

    @staticmethod
    def load_ftps_from_file(file_path: str) -> Strobe:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        x = Strobe()
        x._values = JSONLoader.build_ndarray_dynamic(data)
        x.length = len(x._values)
        x.path = file_path
        return x
            

       
    @staticmethod
    def load_out_from_file(file_path: str) -> Strobe:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        x = Strobe()
        for k, v in data.items():
            re.findall(r'\d+', k)
            arr = list()
            arr.append(k)
            arr.append(v)
            x._values = list(arr)
        x.length = len(x._values)
        x.path = file_path
        return x
            
    @staticmethod
    def load_mseq_from_file(file_path: str) -> Strobe:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        x = Strobe()
        for i in data.items():
            x._values = i
        x.length = len(x._values)
        x.path = file_path