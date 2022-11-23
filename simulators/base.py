from typing import Dict
from types import MethodType

class Simulator:
    X_BASIS = 1
    Y_BASIS = 2
    Z_BASIS = 3

    def __init__(self, nqubits: int) -> None:
        assert nqubits > 0, 'nqubits must be greater that 0'
        self._gates = {}
    
    @property
    def gates(self) -> Dict:
        return self._gates
    
    def add_gate(self, name: str, func) -> None:
        secure_name = f'__{name}'
        self.__dict__[secure_name] = MethodType(func, self)
        self._gates[name] = self.__dict__[secure_name]
    
    def apply_gate(self, gate: str, *args) -> None:
        if gate not in self.gates.keys():
            raise NotImplementedError(f'Gate {gate} it is not implemented in {self.__class__.__name__}')
        self.gates[gate](*args)
    
    def measure(self, target: int, basis: int = Z_BASIS) -> int:
        raise NotImplemented('Unimplemented measure function')
    
    def measure_all(self, basis: int = Z_BASIS) -> str:
        result = ''
        for i in range(self.nqubits):
            result = str(self.measure(i, basis)) + result
        return result