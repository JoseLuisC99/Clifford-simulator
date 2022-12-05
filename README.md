# Clifford simulator

Efficient Clifford simulator using graph state formalism (and non-optimizing state vector simulator) with a lightweight implementation of QASM as interface.

Run the next script for help:

```console
foo@bar:~$ python clifford.py --help
usage: clifford.py [-h] --simulator {statevector,clifford} file

Basic QASM implemetation for Clifford Circuits

positional arguments:
  file                  QASM file program

optional arguments:
  -h, --help            show this help message and exit
  --simulator {statevector,clifford}
```

## Example
```console
foo@bar:~$ python clifford.py ./test/syndrome.qasm --simulator clifford
Counter({'11000': 1000})
```