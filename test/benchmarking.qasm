// One randomized benchmarking sequence
OPENQASM 2.0;


qreg q[2];
creg c[2];
h q[0];
cz q[0],q[1];

s q[0];
cz q[0],q[1];

s q[0];
z q[0];
h q[0];

measure q -> c;
