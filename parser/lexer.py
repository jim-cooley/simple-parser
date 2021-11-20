import copy
from dataclasses import dataclass

from parser import statedef as _

from runtime.keywords import Keywords
from runtime.token import Token
from runtime.token_class import TCL
from runtime.token_data import u16_to_tkid
from runtime.token_ids import TK

_MAX_TOKEN_LEN = 128


@dataclass
class Lexer:

    def __init__(self, source):
        self.keywords = Keywords()
        self._char = None
        self._chid = None
        self.head = 0
        self.length = len(source)
        self.source = source
        self.location = Token.Loc.ZERO()
        self.has_more = True

    def __iter__(self):
        self.get_char()
        return self

    def __next__(self):
        if not self.has_more:
            raise StopIteration
        tk = self._fetch()
        if tk.id == TK.EOF:
            self.has_more = False
        return tk

    def _fetch(self):
        tk = Token.EOF()
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
                    if cs == int(TK.FLOT) and cc == _.CL.DOT:     # double-dot lex glob correction
                        self.head -= 1
                        tk.lexeme = tk.lexeme[:len(tk.lexeme)-1]  # strip the '.' so we can reparse
                        cs = TK.INT
                    # if state transition, don't record but fetch.  If token, don't fetch. don't record
                    fetch = (cs == TK.QUOT) or (cs < _.ST.MAX)    # for quote, remove trailing quote from stream
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
            tk.location = copy.copy(self.location)
            if tk.id == TK.WHT:
                continue
            if tk.id == TK.EOL:
                self.location.line += 1
                self.location.offset = 0
                continue
            elif tk.id == TK.SPEC:
                tk.id = TK(self._chid)
            elif tk.id == TK.EOF:
                self._has_more = False
            break
        if tk.id == TK.IDENT:
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
        c = 0 if self.head >= self.length else ord(self.source[self.head])
        self.head += 1
        return c

    def get_char(self):
        c = self._get_next_char()
        self._chid = c
        self._char = chr(c)
        if c > 0:
            self.location.offset += 1
            if c > 127:
                c = u16_to_tkid[c]
                self._chid = c
        return c
