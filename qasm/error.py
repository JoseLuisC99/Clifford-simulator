class QasmError(Exception):
    pass

class UnsupportedVersion(QasmError):
    pass

class QasmIOError(QasmError, IOError):
    pass
class QasmSyntaxError(QasmError, SyntaxError):
    pass

class EndOfCodeError(QasmIOError):
    pass

class MissingSemicolonError(QasmSyntaxError):
    pass
class MissingIdentifierError(QasmSyntaxError):
    pass
class MissingIntegerError(QasmSyntaxError):
    pass
class MissingRealError(QasmSyntaxError):
    pass
class MalformedExpressionError(QasmSyntaxError):
    pass

class InvalidVersionError(QasmError):
    pass