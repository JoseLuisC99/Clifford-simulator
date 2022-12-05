import sys
from enum import Enum
from itertools import product
from typing import Union
from .register import QuantumRegister, ClassicalRegister, Register as CircRegister, RegisterType
from .error import *

sys.path.append('..')
from qasm.instruction import *

CircuitOp = Enum('CircuitOp', ['APPLY', 'MEASURE', 'IF', 'GATE'])

class QuantumCircuit:
    def __init__(self, qreg: Union[QuantumRegister, List[QuantumRegister]], creg: Union[ClassicalRegister, List[ClassicalRegister]]) -> None:
        if isinstance(qreg, QuantumRegister):
            qreg = [qreg]
        if isinstance(creg, ClassicalRegister):
            creg = [creg]
        
        self._qreg = {}
        self._creg = {}
        self._qsize = 0
        self._csize = 0
        for reg in qreg:
            self._qreg[reg.name] = reg
            reg._offset = self._qsize
            self._qsize += reg.size
        for reg in creg:
            self._creg[reg.name] = reg
            reg._offset = self._csize
            self._csize += reg.size
        self.operations = []

    def _get_qreg(self, name: str) -> QuantumRegister:
        return self._qreg[name]
    
    def _get_creg(self, name: str) -> ClassicalRegister:
        return self._creg[name]
    
    def _resolve_reg(self, reg: CircRegister, idx: int = -1) -> Tuple[int, ...]:
        if idx == -1:
            return tuple(x for x in range(reg._offset, reg._offset + reg.size))
        else:
            if idx >= reg.size:
                raise OutOfBoundsError(f'{reg.id} has not index {idx}')
            return  (reg._offset + idx, )
        
    def _set_bitval(self, idx: int, val: int) -> None:
        for name in self._creg:
            reg = self._creg[name]
            if reg._offset <= idx < reg._offset + reg.size:
                creg = reg
                break
        creg[idx - creg._offset].val = val

    def _apply_operation(self, type: CircuitOp, name: str, *args) -> None:
        self.operations.append((type, name, *args))
    
    def _apply(self, name: str, *args) -> None:
        self._apply_operation(CircuitOp.APPLY, name, *args)
    
    def _apply_measurement(self, qubit: int, bit: int) -> None:
        self._apply_operation(CircuitOp.MEASURE, 'measure', qubit, bit)
    
    def _apply_if(self, val: int, creg: ClassicalRegister, instructions) -> None:
        self._apply_operation(CircuitOp.IF, 'if', val, creg, instructions)
    
    def I(self, qubit: int) -> None:
        self._apply('i', qubit)
    
    def X(self, qubit: int) -> None:
        self._apply('x', qubit)
    
    def Y(self, qubit: int) -> None:
        self._apply('y', qubit)
    
    def Z(self, qubit: int) -> None:
        self._apply('z', qubit)
    
    def H(self, qubit: int) -> None:
        self._apply('h', qubit)
    
    def S(self, qubit: int) -> None:
        self._apply('s', qubit)
    
    def Sdg(self, qubit: int) -> None:
        self._apply('sdg', qubit)
    
    def T(self, qubit: int) -> None:
        self._apply('t', qubit)
    
    def CX(self, control: int, target: int) -> None:
        self._apply('cx', control, target)
    
    def CY(self, control: int, target: int) -> None:
        self._apply('cy', control, target)

    def CZ(self, control: int, target: int) -> None:
        self._apply('cz', control, target)
    
    def Swap(self, control: int, target: int) -> None:
        self._apply('swap', control, target)
    
    def measure(self) -> None:
        for qname, cname in zip(self._qreg, self._creg):
            qidx = self._resolve_reg(self._get_qreg(qname), -1)
            cidx = self._resolve_reg(self._get_creg(cname), -1)
            
            if len(qidx) != len(cidx):
                raise MeasureError('invalid register for measure operation')
            for a, b in zip(qidx, cidx):
                self._apply_measurement(a, b)
    
    @staticmethod
    def from_qasm(qasm: QasmProgram):
        qreg = []
        creg = []

        instructions = []
        for ins in qasm.prog:
            if isinstance(ins, QReg):
                qreg.append(QuantumRegister(ins.size, ins.id))
            elif isinstance(ins, CReg):
                creg.append(ClassicalRegister(ins.size, ins.id))
            else:
                instructions.append(ins)
        circ = QuantumCircuit(qreg, creg)

        def resolve_apply(ins: ApplyGate):
            idxs = []
            for reg in ins.args:
                idxs.append(circ._resolve_reg(circ._get_qreg(reg.id), reg.idx))
            for x in product(*idxs):
                circ._apply(ins.name, *x)

        for ins in instructions:
            if isinstance(ins, ApplyGate):
                resolve_apply(ins)
            elif isinstance(ins, Measure):
                qidx = circ._resolve_reg(circ._get_qreg(ins.qreg.id), ins.qreg.idx)
                cidx = circ._resolve_reg(circ._get_creg(ins.creg.id), ins.creg.idx)
                
                if len(qidx) != len(cidx):
                    raise MeasureError('invalid register for measure operation')
                for a, b in zip(qidx, cidx):
                    circ._apply_measurement(a, b)
            elif isinstance(ins, If):
                body = ins.body
                idxs = []
                for reg in body.args:
                    idxs.append(circ._resolve_reg(circ._get_qreg(reg.id), reg.idx))
                if_apply = []
                for x in product(*idxs):
                    if_apply.append((CircuitOp.APPLY, body.name, *x))
                circ._apply_if(ins.val, circ._get_creg(ins.creg), if_apply)
            else:
                raise NotImplementedError('unimplemented operation for QuantumCircuit')
        
        return circ