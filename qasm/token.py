from typing import Any

class Token:
    Illegal = 0
    EndOfFile = 1
    # Literals
    Real = 2
    Integer = 3
    Id = 4
    # Syntaxis tokens
    OpenQASM = 5
    Semicolon = 6
    Comma = 7
    LParen = 8
    LSParen = 9
    LCParen = 10
    RParen = 11
    RSParen = 12
    RCParen = 13
    Arrow = 14
    Equals = 15
    # Mathematical expressions
    Plus = 16
    Minus = 17
    Times = 18
    Divide = 19
    Power = 20
    Sin = 21
    Cos = 22
    Tan = 23
    Exp = 24
    Ln = 25
    Sqrt = 26
    Pi = 27
    # Reserved words
    QReg = 28
    CReg = 29
    Barrier = 30
    Gate = 31
    Measure = 32
    Reset = 33
    Include = 34
    Opaque = 35
    If = 36
    # Strings
    Filename = 37

    def __init__(self, id: int, data: Any = None, text: str = '') -> None:
        self.id = id
        self.data = data
        self.text = text
    
    def __eq__(self, token: int) -> bool:
        return self.id == token
    
    def __str__(self) -> str:
        if self.data is None:
            return f'<{self.id}>'
        else:
            return f'<{self.id}, {self.data}>'
    
    def __repr__(self) -> str:
        return str(self)

def resolve_identifier(id: str) -> Token:
    if id == 'OPENQASM':
        return Token(Token.OpenQASM)
    # Mathematical expressions
    elif id == 'sin':
        return Token(Token.Sin)
    elif id == 'cos':
        return Token(Token.Cos)
    elif id == 'tan':
        return Token(Token.Tan)
    elif id == 'exp':
        return Token(Token.Exp)
    elif id == 'ln':
        return Token(Token.Ln)
    elif id == 'sqrt':
        return Token(Token.Sqrt)
    elif id == 'pi':
        return Token(Token.Pi)
    # Reserved words
    elif id == 'qreg':
        return Token(Token.QReg)
    elif id == 'creg':
        return Token(Token.CReg)
    elif id == 'barrier':
        return Token(Token.Barrier)
    elif id == 'gate':
        return Token(Token.Gate)
    elif id == 'measure':
        return Token(Token.Measure)
    elif id == 'reset':
        return Token(Token.Reset)
    elif id == 'include':
        return Token(Token.Include)
    elif id == 'opaque':
        return Token(Token.Opaque)
    elif id == 'if':
        return Token(Token.If)
    else:
        return Token(Token.Id, id)
