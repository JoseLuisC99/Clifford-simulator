from argparse import ArgumentParser
from simulators.clifford import GraphStateSimulator
from simulators.statevector import StatevectorSimulator
from qasm.tokenizer import Tokenizer
from qasm.parser import Parser
from lib.executor import Executor
from lib.circuit import QuantumCircuit

if __name__ == '__main__':
    parser = ArgumentParser(description='Basic QASM implemetation for Clifford Circuits')
    parser.add_argument('file', type=str, help='QASM file program')
    parser.add_argument('--simulator', type=str, choices=['statevector', 'clifford'], required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        code = f.read()
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        qasm = parser.parse()
        circ = QuantumCircuit.from_qasm(qasm)
        exec = Executor(circ)
        if args.simulator == 'statevector':
            print(exec.run(StatevectorSimulator))
        elif args.simulator == 'clifford':
            print(exec.run(GraphStateSimulator))