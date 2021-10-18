from dataclasses import dataclass

import copy
import string
from io import RawIOBase, BytesIO
from typing import Optional, List
from symbols import SymbolTable

import statedef as _
from tokens import TK, TCL, Token

_MAX_TOKEN_LEN = 128  # or whatever you please, controls length of identifier among other things


class Lexer(object):
    _char: string = None
    _chid: int = None
    _cline: string = None
    token: Token = None
    symbols: SymbolTable

    def __init__(self, stream=None, string=None, symtab: SymbolTable =None):
        if string is not None:
            stream = BytesIO(bytes(string, 'ascii'))
        if stream is None:
            raise SyntaxError  # must pass stream or string
        self._stream = stream
        self._state = _.ST.MAIN
        self._has_more = True
        self._loc = Token.Loc(0, 0)
        self.symbols = symtab
        if not self._stream.readable():
            raise IOError
        self.get_char()
        pass

    def readable(self) -> bool:
        return self._has_more and self._stream.readable()

    def tell(self):
        return self._loc

    def advance(self, skip_white_space=True, skip_end_of_line=True):
        tk = self._fetch(skip_white_space, skip_end_of_line)
        print(tk.format())
        return tk

    def peek(self):
        if self.token is None:
            self.token = self._fetch()
        return self.token

    # Parsing protocol
    def _fetch(self, skip_white_space=True, skip_end_of_line=True):
        tk = Token(TK.EOF)
        fetch = False

        while True:
            tk.lexeme = ""
            self._state = _.ST.MAIN
            while self._state <= _.ST.MAX:
                cs = self._state
                cs = _.tkState[cs][_.cClass[self._chid]]
                tk.location = copy.copy(self._loc)
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
            if tk.id == TK.EOL:
                self._loc.line += 1
                self._loc.offset = 0
                if not skip_end_of_line:
                    break
            if skip_white_space and tk.id == TK.WHT:
                continue
            break
        if tk.id == TK.IDNT:
            tk.t_class = TCL.IDENTIFIER
            tk =self.symbols.find_add_symbol(tk)
        else:
            tk.t_class = self.symbols.get_tokentype(tk)
        self.token = tk
        if tk.id == TK.EOF:
            self._has_more = False
        return tk

    def _get_next_char(self):
        return 0 if not self.readable() else int.from_bytes(self._stream.read(1), 'big')

    # fetch discards via overwriting
    def get_char(self):
#       self._cline = self.readline() if self._cline is None else self._cline
        self._chid = self._get_next_char()
        if self._chid == 0:
            self._chid = _.CL.EOF
            self._char = chr(self._chid)
        else:
            self._char = chr(self._chid)
#            if self._chid == 13:    # both unix and PC have \r
#                self._loc.line += 1
#                self._loc.offset = 0
            self._loc.offset += 1
        return self._chid
