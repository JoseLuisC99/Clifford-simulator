from typing import Tuple, List
from more_itertools import peekable

from .token import Token
from .tokenizer import Tokenizer
from .instruction import *
from .error import *

class Parser:
    VERSIONS = [2.0]
    def __init__(self, tokens: Tokenizer) -> None:
        self.tokens = peekable(tokens)
    
    def next_token(self) -> Token:
        try:
            return next(self.tokens)
        except StopIteration:
            raise EndOfCodeError('incomplete or invalid source code')
    
    def next_must_be(self, token: int, msg: str = '') -> None:
        try:
            if next(self.tokens) != token:
                raise MalformedExpressionError(msg)
        except StopIteration:
            raise MalformedExpressionError(msg)
    
    def safe_peek(self) -> Token | None:
        try:
            return self.tokens.peek()
        except StopIteration:
            return None
    
    def read_semicolon(self) -> None:
        token = self.next_token()
        if token != Token.Semicolon:
            raise MissingSemicolonError

    def read_identifier(self) -> str:
        token = self.next_token()
        if token != Token.Id:
            raise MissingIdentifierError
        return token.data
    
    def read_id_list(self) -> Tuple[str]:
        ids = []
        ids.append(self.read_identifier())
        while self.safe_peek() == Token.Comma:
            self.next_token()
            ids.append(self.read_identifier())
        
        return ids
    
    def read_integer(self) -> int:
        token = self.next_token()
        if token != Token.Integer:
            raise MissingIntegerError
        return token.data
    
    def read_real(self) -> float:
        token = self.next_token()
        if token != Token.Real:
            raise MissingRealError
        return token.data
    
    def read_argument(self) -> Register:
        identifier = self.read_identifier()
        if self.safe_peek() == Token.LSParen:
            self.next_token()
            n = self.read_integer()
            self.next_must_be(Token.RSParen, 'missing closing bracket')
            return Register(identifier, n)
        else:
            return Register(identifier, -1)
    
    def read_args_list(self) -> List[Register]:
        args = []
        args.append(self.read_argument())
        while self.safe_peek() == Token.Comma:
            self.next_token()
            args.append(self.read_argument())
        return args
    
    def read_mathexpr(self) -> Token:
        # TODO: read math expression
        return Token(Token.Illegal)
    
    def read_mathexpr_list(self) -> Token:
        # TODO: read math expression list
        return Token(Token.Illegal)
    
    def parse(self) -> QasmProgram:
        main = self.parse_header()
        if main.version not in Parser.VERSIONS:
            raise UnsupportedVersion
        
        while self.safe_peek() is not None:
            instruction = self.parse_next()
            main.prog.append(instruction)
        
        return main

    def parse_next(self) -> QInstruction:
        token = self.next_token()
        if token == Token.QReg:
            return self.parse_qreg()
        elif token == Token.CReg:
            return self.parse_creg()
        elif token == Token.Barrier:
            return self.parse_barrier()
        elif token == Token.Reset:
            return self.parse_reset()
        elif token == Token.Measure:
            return self.parse_measure()
        elif token == Token.Id:
            return self.parse_apply(token.data)
        elif token == Token.Opaque:
            return self.parse_opaque()
        elif token == Token.Gate:
            return self.parse_gate()
        elif token == Token.If:
            return self.parse_if()
        else:
            raise MalformedExpressionError(f'unexpected symbol {token.text}')
    
    def parse_header(self) -> QasmProgram:
        self.next_must_be(Token.OpenQASM, 'qasm must start with OPENQASM directive')
        version = self.next_token()
        if version != Token.Real:
            raise InvalidVersionError
        self.read_semicolon()

        return QasmProgram(version.data, [])
    
    def parse_qreg(self) -> QReg:
        id = self.read_identifier()
        self.next_must_be(Token.LSParen, 'missing open square bracket')
        size = self.read_integer()
        self.next_must_be(Token.RSParen, 'missing close square bracket')
        self.read_semicolon()

        return QReg(id, size)
    
    def parse_creg(self) -> CReg:
        id = self.read_identifier()
        self.next_must_be(Token.LSParen, 'missing open square bracket')
        size = self.read_integer()
        self.next_must_be(Token.RSParen, 'missing close square bracket')
        self.read_semicolon()

        return CReg(id, size)
    
    def parse_if(self) -> If:
        self.next_must_be(Token.LParen, 'missing open parenthesis')
        creg = self.read_identifier()
        self.next_must_be(Token.Equals, 'missing equals operator')
        val = self.read_integer()
        self.next_must_be(Token.RParen, 'missing close parenthesis')
        body = self.parse_next()

        return If(creg, val, body)
    
    def parse_barrier(self) -> Barrier:
        qarg = self.read_argument()
        self.read_semicolon()

        return Barrier(qarg)
    
    def parse_reset(self) -> Reset:
        qarg = self.read_argument()
        self.read_semicolon()

        return Reset(qarg)
    
    def parse_measure(self) -> Measure:
        qreg = self.read_argument()
        self.next_must_be(Token.Arrow, 'missing arrow operator')
        creg = self.read_argument()
        self.read_semicolon()

        return Measure(qreg, creg)
    
    def parse_apply(self, id: str) -> ApplyGate:
        params = []
        if self.safe_peek() == Token.LParen:
            self.next_token()
            if self.safe_peek() == Token.RParen:
                self.next_token()
            else:
                params = self.read_mathexpr_list() # Bug here!
                self.next_must_be(Token.RParen)
        args = self.read_args_list()
        self.read_semicolon()
        
        return ApplyGate(id, params, args)
    
    def read_apply_list(self) -> List[ApplyGate]:
        result = []
        while self.safe_peek() == Token.Id:
            gate = self.read_identifier()
            ins = self.parse_apply(gate)
            result.append(ins)
        
        return result
    
    def parse_opaque(self) -> Opaque:
        id = self.read_identifier()
        params = []
        if self.safe_peek() == Token.LParen:
            self.next_token()
            if self.safe_peek() == Token.RParen:
                self.next_token()
            else:
                params = self.read_id_list()
                self.next_must_be(Token.RParen, 'missing close parenthesis')
        args = self.read_id_list()
        self.read_semicolon()

        return Opaque(id, params, args)
    
    def parse_gate(self) -> Gate:
        id = self.read_identifier()
        params = []
        if self.safe_peek() == Token.LParen:
            self.next_token()
            if self.safe_peek() == Token.RParen:
                self.next_token()
            else:
                params = self.read_id_list()
                self.next_must_be(Token.RParen, 'missing close parenthesis')
        args = self.read_id_list()
        self.next_must_be(Token.LCParen, 'missing open curly bracket')

        body = []
        if self.safe_peek() == Token.RCParen:
            self.next_token()
        else:
            body = self.read_apply_list()
            self.next_must_be(Token.RCParen, 'missing close curly bracket')
        
        return Gate(id, params, args, body)

