// Repetition code syndrome measurement
OPENQASM 2.0;

qreg q[3];
qreg a[2];
creg c[3];
creg syn[2];

x q[1]; // error

// Syndrome
cx q[0], a[0];
cx q[1], a[0];
cx q[1], a[1];
cx q[2], a[1];

measure a -> syn;
if(syn==1) x q[0];
if(syn==2) x q[2];
if(syn==3) x q[1];
measure q -> c;