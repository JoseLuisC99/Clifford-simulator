from typing import List, Tuple

class QInstruction:
    def __init__(self) -> None:
        pass

class Register:
    def __init__(self, id: str, idx: int = -1) -> None:
        self.id = id
        self.idx = idx
    def __str__(self) -> str:
        if self.idx != -1:
            return f'{self.id}[{self.idx}]'
        else:
            return self.id

class QasmProgram(QInstruction):
    def __init__(self, version: float, prog: List[QInstruction]) -> None:
        self.version = version
        self.prog = prog
    def __str__(self) -> str:
        s = f'OPENQASM {self.version}\n'
        for p in self.prog:
            s += str(p) + '\n'
        return s

class Include(QInstruction):
    def __init__(self, filename: str) -> None:
        self.filename = filename
    def __str__(self) -> str:
        return f'Include <{self.filename}>'

class QReg(QInstruction):
    def __init__(self, id: str, size: int) -> None:
        self.id = id
        self.size = size
    def __str__(self) -> str:
        return f'QReg {self.id}[{self.size}]'

class CReg(QInstruction):
    def __init__(self, id: str, size: int) -> None:
        self.id = id
        self.size = size
    def __str__(self) -> str:
        return f'CReg {self.id}[{self.size}]'

class Barrier(QInstruction):
    def __init__(self, qreg: Register) -> None:
        self.qreg = qreg
    def __str__(self) -> str:
        return f'Barrier {self.qreg}'

class Reset(QInstruction):
    def __init__(self, qreg: Register) -> None:
        self.qreg = qreg
    def __str__(self) -> str:
        return f'Reset {self.qreg}'

class Measure(QInstruction):
    def __init__(self, qreg: Register, creg: Register) -> None:
        self.qreg = qreg
        self.creg = creg
    def __str__(self) -> str:
        return f'Measure {self.qreg} -> {self.creg}'

class ApplyGate(QInstruction):
    def __init__(self, name: str, params: List[str], args: List[Register]) -> None:
        self.name = name
        self.params = params
        self.args = args
    def __str__(self) -> str:
        params = [str(param) for param in self.params]
        args = [str(arg) for arg in self.args]

        if len(self.params) > 0:
            return f'{self.name} ({",".join(params)}) {",".join(args)}'
        else:
            return f'{self.name} {" ".join(args)}'

class Gate(QInstruction):
    def __init__(self, name: str, params: List[str], args: List[str], body: List[ApplyGate]) -> None:
        self.name = name
        self.params = params
        self.args = args
        self.body = body
    def __str__(self) -> str:
        params = [str(param) for param in self.params]
        args = [str(arg) for arg in self.args]
        
        if len(self.params) > 0:
            s = f'Gate {self.name} ({",".join(params)}) {",".join(args)}'
        else:
            s = f'Gate {self.name} {",".join(args)}'
        
        if len(self.body) > 0:
            s += ' {\n'
            for b in self.body:
                s += '\t' + str(b) + '\n'
            s += '}'
        else:
            s += ' {}'
        return s

class Opaque(QInstruction):
    def __init__(self, name: str, params: List[str], args: List[str]) -> None:
        self.name = name
        self.params = params
        self.args = args
    def __str__(self) -> str:
        params = [str(param) for param in self.params]
        args = [str(arg) for arg in self.args]
        
        if len(self.params) > 0:
            s = f'Opaque {self.name} ({",".join(params)}) {",".join(args)}'
        else:
            s = f'Opaque {self.name} {",".join(args)}'
        return s

class U(QInstruction):
    def __init__(self, phi: float, theta: float, gamma: float, qreg: List[int]) -> None:
        self.phi = phi
        self.theta = theta
        self.gamma = gamma
        self.qreg = qreg

class CX(QInstruction):
    def __init__(self, qcontrol: List[int], qtarget: List[int]) -> None:
        self.qcontrol = qcontrol
        self.qtarget = qtarget

class If(QInstruction):
    def __init__(self, creg: str, val: int, body: ApplyGate) -> None:
        self.creg = creg
        self.val = val
        self.body = body
    def __str__(self) -> str:
        s = f'If ({self.creg} == {self.val})'
        s += '\n\t' + str(self.body)
        return s