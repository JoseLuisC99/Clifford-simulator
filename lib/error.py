class CircuitError(Exception):
    pass
class RegisterError(CircuitError):
    pass
class OutOfBoundsError(RegisterError, IndexError):
    pass
class MeasureError(CircuitError):
    pass