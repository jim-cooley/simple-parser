import copy
from dataclasses import dataclass
from enum import IntEnum

import parser.statedef as _
from runtime.keywords import Keywords
from runtime.token_data import u16_to_tkid
from runtime.token_class import TCL
from runtime.token import Token
from runtime.token_ids import TK

_MAX_TOKEN_LEN = 128


@dataclass
class Lexer:

    class SEEK(IntEnum):
        HEAD = 0
        CURR = 1
        TAIL = 2
        NEXT = 3    # next non-eol
        EOL = 4     # seek to next EOL (+1)

    def __init__(self, source, verbose=False):
        self.keywords = Keywords()
        self._char = None
        self._chid = None
        self.pos = 0
        self.tokens = self._lex(source)
        self._has_more = True
        self._verbose = verbose

    def __iter__(self):
        self.pos = 0
        return self

    def __next__(self):
        if not self._has_more:
            raise StopIteration
        t = self.read1()
        self._has_more = t.id != TK.EOF
        return t

    def get_location(self):
        return self._loc

    def get_tokens(self):
        return self.tokens

    def peek(self, rel=0):
        pos = self.pos + rel
        return self.tokens[pos] if pos < len(self.tokens) else Token.EOF(self._loc)

    def read1(self):
        t = self.tokens[self.pos] if self.pos < len(self.tokens) else Token.EOF(self._loc)
        self.pos += 1
        self._has_more = t.id != TK.EOF
        return t

    def reset(self):
        self.pos = 0
        self._has_more = True

    def seek(self, rel, whence=SEEK.HEAD):
        if whence == Lexer.SEEK.HEAD:
            self.pos = rel
        elif whence == Lexer.SEEK.CURR:
            self.pos += rel
        elif whence == Lexer.SEEK.TAIL:
            self.pos = len(self.tokens) + rel - 1
        elif whence == Lexer.SEEK.NEXT:  # seek to next non-whitespace token
            while self.tokens[self.pos].id == TK.EOL:
                self.pos += 1
                if self.tokens[self.pos].id == TK.EOF:
                    break
        elif whence == Lexer.SEEK.EOL:   # seek just past the next EOL (useful for sync)
            while self.tokens[self.pos].id != TK.EOL:
                self.pos += 1
                if self.tokens[self.pos].id == TK.EOF:
                    self.pos +=1
                    break
        if self.pos > len(self.tokens):
            self.pos = len(self.tokens)
        self._has_more = self.tokens[self.pos].id != TK.EOF
        return self._has_more

    def tell(self):
        return self.pos

    def printall(self):
        tk = None
        idx = 0
        for tk in self.tokens:
            print(f'{idx:5d} : {tk}: line:{tk.location.line}, pos:{tk.location.offset}')
            idx += 1
        self.reset()

    def _lex(self, source):
        self.source = source
        self._len = len(source)
        self._loc = Token.Loc(0, 0)
        self._head = 0
        self.get_char()
        tids = []
        while True:
            tk = self._fetch()
            tids.append(tk)
            if tk.id == TK.EOF:
                break
        return tids

    def _fetch(self):
        tk = Token(TK.EOF)
        fetch = False

        while True:
            tk.lexeme = ""
            cs = self._state = _.ST.MAIN
            while self._state <= _.ST.MAX:
                cs, c = self._state, self._chid
                cc = _.CL.SPEC if c > 127 else _.cClass[c]
                cs = _.tkState[cs][cc]
                if cs < 0:
                    cs = -cs
                    # if state transition, don't record but fetch.  If token, don't fetch. don't record
                    fetch = (cs == TK.QUOT) or (cs < _.ST.MAX)  # for quote, toss trailing quote
                else:
                    tk.lexeme += self._char
                    fetch = True
                    if len(tk.lexeme) > _MAX_TOKEN_LEN:
                        tk.id = TK.ERR
                self._state = cs
                if fetch:
                    fetch = False
                    self.get_char()
            tk.id = TK(cs)
            tk.location = copy.copy(self._loc)
            if tk.id == TK.WHT:
                continue
            if tk.id == TK.EOL:
                self._loc.line += 1
                self._loc.offset = 0
            elif tk.id == TK.SPEC:
                tk.id = TK(self._chid)
            elif tk.id == TK.EOF:
                self._has_more = False
            break
        if tk.id == TK.IDNT:
            tk.t_class = TCL.IDENTIFIER
            tk = self.keywords.find(name=tk.lexeme, default=tk)
            if not isinstance(tk, Token):
                tk = tk.token
            tk = copy.deepcopy(tk)
        else:
            tk.remap2tclass()
        self.token = tk
        if tk.id == TK.EOF:
            self._has_more = False
        return tk

    def _get_next_char(self):
        c = 0 if self._head >= self._len else ord(self.source[self._head])
        self._head += 1
        return c

    def get_char(self):
        c = self._get_next_char()
        self._chid = c
        self._char = chr(c)
        if c > 0:
            self._loc.offset += 1
            if c > 127:
                c = u16_to_tkid[c]
                self._chid = c
        return c


def _tk_copy(token, loc=None):
    tk = copy.copy(token)
    if loc is not None:
        tk.location = copy.copy(loc)
    return tk