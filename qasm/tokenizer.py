from .token import Token, resolve_identifier
from .error import QasmSyntaxError

class Tokenizer:
    def __init__(self, input) -> None:
        self.input = list(input)
        self.idx = -1
    
    def read(self) -> str:
        self.idx += 1
        if self.idx >= len(self.input):
            return None
        return self.input[self.idx]
    
    def peek(self) -> str:
        if self.idx + 1 >= len(self.input):
            return None
        return self.input[self.idx + 1]
    
    def skip_whitespace(self) -> None:
        while self.peek() is not None and self.peek().isspace():
            self.read()
    
    def skip_comment(self) -> None:
        while self.peek() is not None and self.peek() != '\n':
            self.read()
    
    def read_id(self, first: str) -> str:
        id = first
        while self.peek().isalnum() or self.peek() == '_':
            id += self.read()
        return id
    
    def read_number(self, first: str) -> str:
        number = first
        while True:
            peek = self.peek()
            if not peek.isnumeric() and peek != '.':
                break
            number += self.read()
        return number
    
    def read_filename(self) -> str:
        filename = ''
        while self.peek() is not None and self.peek() != '"':
            filename += self.read()
        self.read() # Skip last "
        return filename
    
    def next(self) -> Token:
        self.skip_whitespace()
        c = self.read()
        if c is None:
            return Token(Token.EndOfFile)
        elif c == '=':
            if self.peek() == '=':
                self.read()
                return Token(Token.Equals, text='==')
            else:
                raise QasmSyntaxError('missing equal sign')
        elif c == '+':
            return Token(Token.Plus, text=c)
        elif c == '-':
            if self.peek() == '>':
                self.read()
                return Token(Token.Arrow, text='->')
            else:
                return Token(Token.Minus, text=c)
        elif c == '*':
            return Token(Token.Times, text=c)
        elif c == '/':
            if self.peek() == '/':
                self.skip_comment()
                return self.next()
            else:
                return Token(Token.Divide, text=c)
        elif c == '^':
            return Token(Token.Power, text=c)
        elif c == ';':
            return Token(Token.Semicolon, text=c)
        elif c == ',':
            return Token(Token.Comma, text=c)
        elif c == '(':
            return Token(Token.LParen, text=c)
        elif c == '[':
            return Token(Token.LSParen, text=c)
        elif c == '{':
            return Token(Token.LCParen, text=c)
        elif c == ')':
            return Token(Token.RParen, text=c)
        elif c == ']':
            return Token(Token.RSParen, text=c)
        elif c == '}':
            return Token(Token.RCParen, text=c)
        elif c == '"':
            filename = self.read_filename()
            return Token(Token.Filename, filename)
        elif c.isalpha() or c == '_':
            identifier = self.read_id(c)
            return resolve_identifier(identifier)
        elif c.isnumeric():
            num = self.read_number(c)
            if '.' in num:
                num = float(num)
                return Token(Token.Real, num)
            else:
                num = int(num)
                return Token(Token.Integer, num)
        else:
            return Token(Token.Illegal)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        token = self.next()
        if token == Token(Token.EndOfFile):
            raise StopIteration
        else:
            return token