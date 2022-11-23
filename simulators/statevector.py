import numpy as np
from numpy import linalg
from functools import reduce
from .base import Simulator

class StatevectorSimulator(Simulator):
    def __init__(self, nqubits: int) -> None:
        super().__init__(nqubits)
        self.nqubits = nqubits
        self.qstate = np.zeros(2 ** nqubits, dtype=complex)
        self.qstate[0] = complex(1.0, 0.0)
        self._gates = {
            # Pauli gates
            'i': self.I, 'x': self.X, 'y': self.Y, 'z': self.Z,
            # Clifford gates
            'h': self.H, 's': self.S, 'sdg': self.Sdg,
            # Multiqubit gates
            'cx': self.CX, 'cy': self.CY, 'cz': self.CZ, 'swap': self.Swap
        }
    
    def __len__(self):
        return 2 ** self.nqubits

    def __getitem__(self, idx) -> complex:
        return self.qstate[idx]
    
    def _apply(self, gates: np.ndarray) -> None:
        self.qstate = gates @ self.qstate
    
    def _apply_unitary(self, gate: np.ndarray, qubit: int) -> None:
        assert 0 <= qubit < self.nqubits, 'qubit out of range'
        
        gates = [np.array([[1, 0],[0 ,1]])] * self.nqubits
        gates[qubit] = gate
        self._apply(reduce(np.kron, gates))
    
    def _apply_controlled(self, gate: np.ndarray, control: int, target: int) -> None:
        assert (0 <= control < self.nqubits) and (0 <= target < self.nqubits), 'qubits out of range'
        assert control != target, 'control qubit must be different from target qubit'

        gates_00 = [np.array([[1, 0],[0 ,1]])] * self.nqubits
        gates_11 = [np.array([[1, 0],[0 ,1]])] * self.nqubits
        gates_00[control] = np.array([[1, 0], [0, 0]])
        gates_11[control] = np.array([[0, 0], [0, 1]])
        gates_11[target] = gate

        self._apply(reduce(np.kron, gates_00) + reduce(np.kron, gates_11))
    
    def I(self, qubit: int) -> None:
        self._apply_unitary(np.array([[1, 0], [0, 1]]), qubit)
    
    def X(self, qubit: int) -> None:
        self._apply_unitary(np.array([[0, 1], [1, 0]]), qubit)
    
    def Y(self, qubit: int) -> None:
        self._apply_unitary(np.array([[0, -1.j], [1.j, 0]]), qubit)
    
    def Z(self, qubit: int) -> None:
        self._apply_unitary(np.array([[1, 0], [0, -1]]), qubit)
    
    def H(self, qubit: int) -> None:
        self._apply_unitary((1/np.sqrt(2)) * np.array([[1, 1], [1, -1]]), qubit)
    
    def S(self, qubit: int) -> None:
        self._apply_unitary(np.array([[1, 0], [0, 1.j]]), qubit)
    
    def Sdg(self, qubit: int) -> None:
        self._apply_unitary(np.array([[1, 0], [0, -1.j]]), qubit)
    
    def CX(self, control: int, target: int) -> None:
        self._apply_controlled(np.array([[0, 1], [1, 0]]), control, target)
    
    def CY(self, control: int, target: int) -> None:
        self._apply_controlled(np.array([[0, -1.j], [1.j, 0]]), control, target)
    
    def CZ(self, control: int, target: int) -> None:
        self._apply_controlled(np.array([[1, 0], [0, -1]]), control, target)
    
    def Swap(self, control: int, target: int) -> None:
        self.CX(control, target)
        self.CX(target, control)
        self.CX(control, target)
    
    def _measure_z(self, target: int) -> int:
        step_size = len(self) // 2 ** (target + 1)
        n_steps = (len(self) // step_size) // 2

        zeros_mask = np.tile(
            np.concatenate((np.ones(step_size), np.zeros(step_size))), n_steps
        )
        ones_mask = np.tile(
            np.concatenate((np.zeros(step_size), np.ones(step_size))), n_steps
        )
        zero_amplitude = np.sum(np.abs(self.qstate * zeros_mask) ** 2)
        one_amplitude = np.sum(np.abs(self.qstate * ones_mask) ** 2)

        measure = np.random.choice([0, 1], p=[zero_amplitude, one_amplitude])
        if measure == 0:
            self.qstate[ones_mask == 1] = 0
        else:
            self.qstate[zeros_mask == 1] = 0
        self.qstate = self.qstate / linalg.norm(self.qstate)
        
        return measure
    
    def measure(self, target: int, basis: int = Simulator.Z_BASIS) -> int:
        assert 0 <= target < self.nqubits, 'qubit out of range'

        if basis == Simulator.Z_BASIS:
            return self._measure_z(target)
        else:
            raise NotImplementedError('Statevector simulator only supports measure on Z basis')