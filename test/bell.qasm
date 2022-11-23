// Repetition code syndrome measurement
OPENQASM 2.0;

qreg b00[2];
qreg b01[2];
qreg b10[2];
qreg b11[2];

creg c00[2];
creg c01[2];
creg c10[2];
creg c11[2];

// Bell state $\beta_{00}$
h b00[0];
cx b00[0], b00[1];

// Bell state $\beta_{01}$
h b01[0];
x b01[1];
cx b01[0], b01[1];

// Bell state $\beta_{10}$
x b10[0];
h b10[0];
cx b10[0], b10[1];

// Bell state $\beta_{11}$
x b11[0];
x b11[1];
h b11[0];
cx b11[0], b11[1];

measure b00 -> c00;
measure b01 -> c01;
measure b10 -> c10;
measure b11 -> c11;