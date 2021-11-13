from dataclasses import dataclass

from numpy import sort, unique

from runtime.token_data import _tk2binop, _tk2lit, _tk2unop, _tk2type, _tk2glyph
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


    # --------------------------
    # Token constructors
    # --------------------------
    # The goal is to use this as the definitive list of valid tokens, then to use that list to generate
    # _tk2type and _tk2glyph.  The mapping dictionaries _tk2binop and _tk2unop should just be subsumed by
    # eliminating the mapped token values and using the right tokens in the lexer.  This will "mess up" the
    # state transition table, so perhaps a compromise can be found to preserve its layout.
    #
    # CONSIDER: the other thought is to take all of this underlying data and build a single table (that could contain
    # more fields), then generate this as well as any required mapping tables.  Also, would be good to get the
    # notation printer's data connected to this somehow as well.
    @staticmethod
    def ANON(loc=None, lex=None):
        return Token(tid=TK.ANON, tcl=TCL.IDENTIFIER, lex=lex or '_', loc=loc)

    @staticmethod
    def APPLY(loc=None, lex=None):
        return Token(tid=TK.APPLY, tcl=TCL.UNARY, lex=lex or '>>', loc=loc)

    @staticmethod
    def ASSIGN(loc=None):
        return Token(tid=TK.ASSIGN, tcl=TCL.FUNCTION, lex='=', val=None, loc=loc)

    @staticmethod
    def ADD(loc=None, value=None):
        return Token(tid=TK.ADD, tcl=TCL.BINOP, lex='+', val=value or False, loc=loc)

    @staticmethod
    def ALL(loc=None, value=None):
        return Token(tid=TK.ALL, tcl=TCL.UNARY, lex='all:', val=value or False, loc=loc)

    @staticmethod
    def AND(loc=None, value=None):
        return Token(tid=TK.AND, tcl=TCL.BINOP, lex='and', val=value or False, loc=loc)

    @staticmethod
    def ANY(loc=None, value=None):
        return Token(tid=TK.ANY, tcl=TCL.UNARY, lex='any:', val=value or False, loc=loc)

    @staticmethod
    def BOOL(loc=None, value=None):
        return Token(tid=TK.BOOL, tcl=TCL.SCOPE, val=value or False, loc=loc)

    @staticmethod
    def BLOCK(loc=None):
        return Token(tid=TK.BLOCK, tcl=TCL.SCOPE, loc=loc)

    # in _tk2binop -> TK.DEFINE
    # def TK.COEQ

    @staticmethod
    def CHAIN(loc=None):
        return Token(tid=TK.CHAIN, tcl=TCL.BINOP, lex='|', loc=loc)

    @staticmethod
    def COLN(loc=None):
        return Token(tid=TK.COLN, tcl=TCL.BINOP, lex=':', loc=loc)

    @staticmethod
    def COMMAND(loc=None):
        return Token(tid=TK.COMMAND, tcl=TCL.UNARY, lex='%%', loc=loc)

    @staticmethod
    def DECREMENT(loc=None):
        return Token(tid=TK.DECREMENT, tcl=TCL.UNARY, lex='--', val=None, loc=loc)

    @staticmethod
    def DEF(loc=None):
        return Token(tid=TK.DEF, tcl=TCL.IDENTIFIER, val=None, loc=loc)

    @staticmethod
    def DEFINE(loc=None):
        return Token(tid=TK.DEFINE, tcl=TCL.FUNCTION, lex=':=', val=None, loc=loc)

    @staticmethod
    def DIV(loc=None):
        return Token(tid=TK.DIV, tcl=TCL.BINOP, lex='/', loc=loc)

    @staticmethod
    def DLRS(loc=None):
        return Token(tid=TK.DLRS, tcl=TCL.UNARY, lex='$', loc=loc)

    @staticmethod
    def DOT(loc=None):
        return Token(tid=TK.DOT, tcl=TCL.BINOP, lex='.', loc=loc)

    @staticmethod
    def DUR(loc=None):
        return Token(tid=TK.DUR, tcl=TCL.LITERAL, val=None, loc=loc)

    @staticmethod
    def ELSE(loc=None):
        return Token(tid=TK.ELSE, tcl=TCL.BINOP, lex='else', loc=loc)

    @staticmethod
    def EMPTY(loc=None):
        return Token(tid=TK.EMPTY, tcl=TCL.LITERAL, lex='{}', val={}, loc=loc)

    @staticmethod
    def EOF(loc=None):
        return Token(tid=TK.EOF, tcl=TCL.LITERAL, lex='', val=None, loc=loc)

    # in _tk2binop -> TK.ASSIGN
    # def TK.EQLS

    # in _tk2binop -> TK.NOT
    # def TK.EXCL

    # in _tk2binop -> TK.POW
    # def TK.EXPN

    @staticmethod
    def FALL_BELOW(loc=None):
        return Token(tid=TK.FALL_BELOW, tcl=TCL.BINOP, lex='<|', loc=loc)

    @staticmethod
    def FALSE(loc=None):
        return Token(tid=TK.BOOL, tcl=TCL.LITERAL, lex='false', val=False, loc=loc)

    @staticmethod
    def FLOT(loc=None):
        return Token(tid=TK.FLOT, tcl=TCL.LITERAL, lex='', val=None, loc=loc)

    @staticmethod
    def FNCALL(name=None, loc=None):
        return Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex=name, loc=loc)

    @staticmethod
    def FUNCTION(name=None, tid=None, loc=None):
        return Token(tid=tid or TK.IDNT, tcl=TCL.FUNCTION, lex=name, loc=loc)

    @staticmethod
    def GTE(name=None, tid=None, loc=None):
        return Token(tid=TK.GTE, tcl=TCL.BINOP, lex='>=', loc=loc)

    @staticmethod
    def GTR(name=None, tid=None, loc=None):
        return Token(tid=TK.GTR, tcl=TCL.BINOP, lex='>', loc=loc)

    @staticmethod
    def IDEV(loc=None):
        return Token(tid=TK.IDIV, tcl=TCL.BINOP, lex='div', loc=loc)

    @staticmethod
    def IF(loc=None):
        return Token(tid=TK.IF, tcl=TCL.BINOP, lex='if', loc=loc)

    @staticmethod
    def IN(loc=None):
        return Token(tid=TK.IN, tcl=TCL.BINOP, lex='in', loc=loc)

    @staticmethod
    def INCREMENT(loc=None):
        return Token(tid=TK.INCREMENT, tcl=TCL.UNARY, lex='++', val=None, loc=loc)

    @staticmethod
    def INDEX(loc=None):
        return Token(tid=TK.INDEX, tcl=TCL.BINOP, lex="[", loc=loc)

    @staticmethod
    def INT(loc=None):
        return Token(tid=TK.INT, tcl=TCL.LITERAL, lex='', val=None, loc=loc)

    @staticmethod
    def ISEQ(loc=None):
        return Token(tid=TK.ISEQ, tcl=TCL.BINOP, lex="==", loc=loc)

    # in _tk2binop -> TK.FALL_BELOW
    # def LBAR

    @staticmethod
    def LESS(value=None, loc=None):
        return Token(tid=TK.LESS, tcl=TCL.BINOP, lex='<', val=value, loc=loc)

    @staticmethod
    def LIST(value=None, loc=None):
        return Token(tid=TK.LIST, tcl=TCL.LITERAL, lex='', val=value, loc=loc)

    @staticmethod
    def LTE(value=None, loc=None):
        return Token(tid=TK.LTE, tcl=TCL.BINOP, lex='<=', val=value, loc=loc)

    @staticmethod
    def MNEQ(loc=None):
        return Token(tid=TK.MNEQ, tcl=TCL.BINOP, lex="+=", loc=loc)

    @staticmethod
    def MOD(loc=None):
        return Token(tid=TK.MOD, tcl=TCL.BINOP, lex='mod', val=None, loc=loc)

    @staticmethod
    def MUL(loc=None):
        return Token(tid=TK.MUL, tcl=TCL.BINOP, lex='*', val=None, loc=loc)

    @staticmethod
    def NEG(loc=None):
        return Token(tid=TK.NEG, tcl=TCL.UNARY, lex='-', val=None, loc=loc)

    @staticmethod
    def NEQ(loc=None):
        return Token(tid=TK.NEQ, tcl=TCL.BINOP, lex="!=", loc=loc)

    @staticmethod
    def NONE(loc=None):
        return Token(tid=TK.NONE, tcl=TCL.LITERAL, lex='', val=None, loc=loc)

    @staticmethod
    def NONEOF(loc=None):
        return Token(tid=TK.NONEOF, tcl=TCL.UNARY, lex='none:', val=None, loc=loc)

    @staticmethod
    def NOT(loc=None):
        return Token(tid=TK.NOT, tcl=TCL.UNARY, lex='not', val=None, loc=loc)

    # UNDONE: shouldn't be a token, just an identifier / intrinsic
    @staticmethod
    def NOW(loc=None):
        return Token(tid=TK.NOW, tcl=TCL.FUNCTION, lex='now', val=None, loc=loc)

    @staticmethod
    def OBJECT(loc=None):
        return Token(tid=TK.OBJECT, tcl=TCL.LITERAL, lex='', val=None, loc=loc)

    @staticmethod
    def OR(loc=None):
        return Token(tid=TK.OR, tcl=TCL.BINOP, lex='or', val=None, loc=loc)

    @staticmethod
    def PCT(loc=None):
        return Token(tid=TK.PCT, tcl=TCL.UNARY, lex="%", loc=loc)

    @staticmethod
    def PLEQ(loc=None):
        return Token(tid=TK.PLEQ, tcl=TCL.BINOP, lex="+=", loc=loc)

    @staticmethod
    def POS(loc=None):
        return Token(tid=TK.POS, tcl=TCL.UNARY, lex='+', val=None, loc=loc)

    @staticmethod
    def POW(loc=None):
        return Token(tid=TK.POW, tcl=TCL.BINOP, lex='^', loc=loc)

    @staticmethod
    def PRODUCE(loc=None):
        return Token(tid=TK.PRODUCE, tcl=TCL.BINOP, lex='=>', loc=loc)

    @staticmethod
    def RAISE(loc=None, lex=None):
        return Token(tid=TK.RAISE, tcl=TCL.UNARY, lex=lex or '->', loc=loc)

    @staticmethod
    def RANGE(loc=None):
        return Token(tid=TK.RANGE, tcl=TCL.BINOP, lex='..', loc=loc)

    @staticmethod
    def REF(loc=None):
        return Token(tid=TK.REF, tcl=TCL.BINOP, lex=".", loc=loc)

    @staticmethod
    def RETURN(loc=None):
        return Token(tid=TK.RETURN, tcl=TCL.UNARY, lex='return', loc=loc)

    @staticmethod
    def RISE_ABOVE(loc=None):
        return Token(tid=TK.RISE_ABOVE, tcl=TCL.BINOP, lex='|>', loc=loc)

    @staticmethod
    def SET(value=None, loc=None):
        return Token(tid=TK.SET, tcl=TCL.LITERAL, lex='', val=value, loc=loc)

    @staticmethod
    def STR(value=None, loc=None):
        return Token(tid=TK.STR, tcl=TCL.LITERAL, lex='', val=value, loc=loc)

    @staticmethod
    def SUB(value=None, loc=None):
        return Token(tid=TK.SUB, tcl=TCL.BINOP, lex='', val=value, loc=loc)

    @staticmethod
    def THEN(loc=None):
        return Token(tid=TK.THEN, tcl=TCL.BINOP, lex='then', loc=loc)

    @staticmethod
    def TIME(value=None, loc=None):
        return Token(tid=TK.TIME, tcl=TCL.LITERAL, lex='', val=value, loc=loc)

    # UNDONE: shouldn't be a token, just an identifier / intrinsic
    @staticmethod
    def TODAY(value=None, loc=None):
        return Token(tid=TK.TODAY, tcl=TCL.FUNCTION, lex='', val=value, loc=loc)

    @staticmethod
    def TRUE(loc=None):
        return Token(tid=TK.BOOL, tcl=TCL.LITERAL, lex='true', val=True, loc=loc)

    @staticmethod
    def TUPLE(loc=None):
        return Token(TK.TUPLE, tcl=TCL.TUPLE, lex='', val=None, loc=loc)

    @staticmethod
    def VAR(value=None, loc=None):
        return Token(tid=TK.VAR, tcl=TCL.UNARY, lex='', val=value, loc=loc)

    @staticmethod
    def WHT(loc=None):
        return Token(tid=TK.WHT, tcl=TCL.NONE, lex='', val=None, loc=loc)
