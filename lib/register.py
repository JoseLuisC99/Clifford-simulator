from .error import *
from enum import Enum
from typing import Union

class Bit:
    def __init__(self) -> None:
        self._val = 0
    
    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, value: int):
        assert value in [1, 0], 'bit only accepts 1 or 0 as values'
        self._val = value

class Qubit:
    def __init__(self) -> None:
        self._collapsed = False
    
    @property
    def val(self):
        return self._collapsed

RegisterType = Enum('RegisterType', ['Classical', 'Quantum'])
class Register:

    def __init__(self, size: int, name: str, type: RegisterType) -> None:
        assert 0 < size, 'size of register must be positive'
        assert type == RegisterType.Classical or type == RegisterType.Quantum, 'invalid register type'
        
        self.size = size
        self.name = name
        self.type = type
        if type == RegisterType.Classical:
            self.register = [Bit() for _ in range(size)]
        else:
            self.register = [Qubit() for _ in range(size)]
        
        # Simulator helper
        self._offset = 0
    
    def qasm(self) -> str:
        return f'{self.type}reg {self.name}[{self.size}]'
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, idx) -> Union[Bit, Qubit]:
        return self.register[idx]
    
    def __iter__(self) -> object:
        for r in self.register:
            yield r

class ClassicalRegister(Register):
    def __init__(self, size: int, name: str) -> None:
        super().__init__(size, name, RegisterType.Classical)
    
    def to_binary_string(self) -> str:
        s = ''
        for b in self.register:
            s = str(b.val) + s
        return s
    
    def to_int(self) -> int:
        return int(self.to_binary_string(), 2)

class QuantumRegister(Register):
    def __init__(self, size: int, name: str) -> None:
        super().__init__(size, name, RegisterType.Quantum)
    
    def collapse(self, qidx: int):
        return None