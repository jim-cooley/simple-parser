from dataclasses import dataclass

from runtime.token_data import _tk2binop, _tk2lit, _tk2unop, _tk2type
from runtime.token_class import TCL
from runtime.token_ids import TK


@dataclass
class Token:
    @dataclass
    class Loc:
        def __init__(self, line=0, offset=0):
            self.line = line
            self.offset = offset

    def __init__(self, tid, tcl=None, lex="", val=None, loc=None, reserved=False):
        self.id = tid
        self.t_class: TCL = TCL(tcl) if tcl is not None else TCL.NONE
        self.lexeme = lex
        self.value = val
        self.location = loc if loc is not None else Token.Loc()
        self.is_reserved = reserved

    def __repr__(self):
        return self.format()

    def __str__(self):
        return self.format()

    def is_equal(self, other):
        if type(other) == type(self):
            if other.t_class == self.t_class:
                if other.value == self.value:
                    return True
        return False

    def set_id(self, tid):
        self.id = tid
        return self

    def map2binop(self):
        return self._map(_tk2binop)

    def map2litval(self):
        return self._map(_tk2lit)

    def remap2binop(self):
        self.id = self._map(_tk2binop)
        return self

    def remap2unop(self):
        self.id = self._map(_tk2unop)
        return self

    def remap2litval(self):
        self.id = self._map(_tk2lit)
        return self

    def remap2tclass(self):
        self.t_class = self._map(_tk2type)
        return self

    def format(self):
        _tn = f'.{self.id.name}(' if hasattr(self.id, "name") else f'({self.id}, '
        _tcl = f'{self.t_class.name}' if hasattr(self.t_class, "name") else 'TCL({self.t_type})'
        _tv = 'None' if self.value is None else f'{self.value}'
        _tl = f'\'{self.lexeme}\'' if self.lexeme is not None else 'None'
        if _tl == '\'\n\'':
            _tl = "'\\n'"
        #       _tloc = f'line:{self.location.line + 1}, pos:{self.location.offset - 1}'
        return f'TK{_tn}{_tcl}, {_tl}, V={_tv})'

    def _map(self, tk_map):
        if self.id in tk_map:
            return tk_map[self.id]
        else:
            return self.id

    def _map_cl(self, tcl_map):
        if self.id in tcl_map:
            return tcl_map[self.id]
        else:
            return self.t_class

    @staticmethod
    def format_token(tk):
        return tk.format()

    @staticmethod
    def format_tid(tk):
        return f'TK.{tk.name}' if hasattr(tk, "name") else f'TK({tk})'

    @staticmethod
    def format_tt(tt):
        return f'TT.{tt.name}' if hasattr(tt, "name") else f'TT({tt})'


TK_EOF = Token(TK.EOF, TCL.LITERAL, '', None)
TK_EMPTY = Token(TK.EMPTY, TCL.LITERAL, '{}', {})
TK_NONE = Token(TK.NONE, TCL.LITERAL, '', None)
TK_SET = Token(TK.SET, TCL.LITERAL, '{', None)
TK_ASSIGN = Token(TK.ASSIGN, TCL.FUNCTION)
TK_DEFINE = Token(TK.DEFINE, TCL.FUNCTION)