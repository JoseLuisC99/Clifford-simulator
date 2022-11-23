// GHZ 3-qubit state
OPENQASM 2.0;

qreg q[3];
creg c[3];

h q[0];
cx q[0], q[1];
cx q[1], q[2];

measure q -> c;