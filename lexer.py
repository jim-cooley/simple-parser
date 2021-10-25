from dataclasses import dataclass

import copy
import string
from io import BytesIO

import statedef as _
from tokens import TK, TCL, Token, u16_to_tkid

_MAX_TOKEN_LEN = 128  # or whatever you please, controls length of identifier among other things


class Lexer(object):

    def __init__(self, code, keywords=None, verbose=True):
        self._char: string = None
        self._chid: int = None
        self._cline: string = None
        self._has_more = True
        self.token: Token = None
        self.text = code
        self._len = len(code)
        self._head = 0
        self._loc = Token.Loc(0, 0)
        self._skip_end_of_line = True
        self.keywords = keywords
        self._verbose = verbose
        self._state = _.ST.MAIN
        self.get_char()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.readable():
            raise StopIteration
        return self.advance(skip_white_space=True, skip_end_of_line=False)

    def readable(self) -> bool:
        return self._has_more  # has more is true until we return one TK.EOF

    def tell(self):
        return self._loc

    def advance(self, skip_white_space=True, skip_end_of_line=True):
        tk = self._fetch(skip_white_space, skip_end_of_line)
        if self._verbose:
            print(tk.format())
        return tk

    def peek(self):
        if self.token is None:
            self.token = self._fetch()
        return self.token

    def seek(self, rel):
        self._head += (rel - 1)
        self._head = -1 if self._head < 0 else self._head
        self.token = self._fetch()
        self._loc.offset += rel
        self._loc.offset = 0 if self._loc.offset < 0 else self._loc.offset

    # Parsing protocol
    def _fetch(self, skip_white_space=True, skip_end_of_line=True):
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
            if not skip_white_space or tk.id == TK.WHT:
                continue
            if tk.id == TK.EOL:
                self._loc.line += 1
                self._loc.offset = 0
                if skip_end_of_line:
                    continue
            elif tk.id == TK.SPEC:
                tk.id = TK(self._chid)
            elif tk.id == TK.EOF:
                self._has_more = False
            break
        if tk.id == TK.IDNT:
            tk.t_class = TCL.IDENTIFIER
            tk = self.keywords.find(tk, tk)
        else:
            tk.map2tclass()
        self.token = tk
        if tk.id == TK.EOF:
            self._has_more = False
        return tk

    def _get_next_char(self):
        c = 0 if self._head >= self._len else ord(self.text[self._head])
        self._head += 1
        return c

    # fetch discards via overwriting
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
