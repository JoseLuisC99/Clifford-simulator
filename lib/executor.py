from collections import Counter
from qasm.parser import *
from lib.circuit import QuantumCircuit, CircuitOp

class Executor:
    def __init__(self, circuit: QuantumCircuit) -> None:
        self.circ = circuit
    
    def run(self, backend, shots: int = 1000) -> Counter:
        assert shots > 1, 'you must execute almost one run'
        result = []
        for _ in range(shots):
            sim = backend(self.circ._qsize)

            for op, name, *args in self.circ.operations:
                if op == CircuitOp.APPLY:
                    sim.apply_gate(name, *args)
                elif op == CircuitOp.MEASURE:
                    b = sim.measure(args[0])
                    self.circ._set_bitval(args[1], b)
                elif op == CircuitOp.IF:
                    bval = args[1].to_int()
                    if args[0] == bval:
                        for op, name, *args in args[2]:
                            sim.apply_gate(name, *args)
            res = ''
            for name in self.circ._creg:
                res = self.circ._creg[name].to_binary_string() + res
            result.append(res)
        
        return Counter(result)