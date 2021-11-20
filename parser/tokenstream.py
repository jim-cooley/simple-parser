from dataclasses import dataclass
from enum import IntEnum

from parser.lexer import Lexer
from runtime.token import Token
from runtime.token_ids import TK


@dataclass
class TokenStream:

    class SEEK(IntEnum):
        HEAD = 0
        CURR = 1
        EOL = 2
        TAIL = 3

    def __init__(self, source):
        self.tokens = self._lex(source)
        self.has_more = True
        self.location = Token.Loc.ZERO()
        self.length = len(self.tokens)
        self.pos = 0

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        if not self.has_more:
            raise StopIteration
        t = self.read1()
        self.has_more = t.id != TK.EOF
        return t

    def peek(self, rel=0):
        pos = self.pos + rel
        if pos < self.length:
            return self.tokens[pos]
        return Token.EOF()

    def read1(self):
        if self.pos < self.length:
            t = self.tokens[self.pos]
            self.pos += 1
            self.has_more = t == TK.EOF
            return t
        return Token.EOF()

    def reset(self):
        self.pos = 0
        self.has_more = True
        self.location = Token.Loc.ZERO()

    def seek(self, rel, whence=SEEK.HEAD):
        if whence == TokenStream.SEEK.HEAD:
            self.pos = rel
        elif whence == TokenStream.SEEK.CURR:
            self.pos += rel
        elif whence == TokenStream.SEEK.TAIL:
            self.pos = self.length + rel - 1
        elif whence == Lexer.SEEK.EOL:   # seek just past the next EOL (useful for sync)
            while self.tokens[self.pos].id != TK.EOL:
                self.pos += 1
                if self.tokens[self.pos].id == TK.EOF:
                    break
        if self.pos > self.length:
            self.pos = self.length
        self.has_more = self.tokens[self.pos].id != TK.EOF
        return self.has_more

    def tell(self):
        return self.pos

    def printall(self):
        tk = None
        idx = 0
        for tk in self:
            print(f'{idx:5d} : {tk}: line:{tk.location.line}, pos:{tk.location.offset}')
            idx += 1
        print('\n\n')
        self.reset()

    def _lex(self, source):
        lexer = Lexer(source)
        tids = [tk for tk in lexer]
        return tids
