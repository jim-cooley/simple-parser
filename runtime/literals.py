from dataclasses import dataclass
from functools import total_ordering

from runtime.scope import Object
from runtime.token_class import TCL
from runtime.token import Token
from runtime.token_ids import TK


@dataclass
class Literal(Object):
    def __init__(self, value=None, token=None, tid=None, loc=None, parent=None):
        if token is None:
            if tid is not None:
                token = Token(tid=tid, tcl=TCL.LITERAL, val=value, loc=loc)
            else:
                token = Token(tid=TK.OBJECT, tcl=TCL.LITERAL, val=value, loc=loc)
        else:
            tid = token.map2litval() if tid is None else tid
            token.t_class = TCL.LITERAL
            token.id = tid
        super().__init__(value=value, parent=parent, token=token)

    # special values
    @staticmethod
    def NONE(loc=None):
        return Literal(token=Token.NONE(loc=loc))

    @staticmethod
    def EMPTY(loc=None):
        return Literal(token=Token.EMPTY(loc=loc))


@dataclass
@total_ordering
class Bool(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.BOOL if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = _parse_bool_value(self._value)

    def __lt__(self, other):
        if isinstance(other, bool):
            return True if self._value < other else False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, bool):
            return True if self._value is other else False
        return NotImplemented

    @staticmethod
    def FALSE(loc=None):
        return Bool(value=False, token=Token.FALSE(loc=loc))

    @staticmethod
    def TRUE(loc=None):
        return Bool(value=True, token=Token.TRUE(loc=loc))

    def format(self, brief=True):
        if self._value is not None:
            if self._value:
                return 'true'
        return 'false'


@dataclass
class Float(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.FLOT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = float(self._value)

    def format(self, brief=True, fmt=None):
        return f'{self._value}'


@dataclass
@total_ordering
class Int(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.INT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        self._value = value
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = int(self._value)

    def __lt__(self, other):
        if isinstance(other, int):
            return True if self._value < other else False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, int):
            return True if self._value == other else False
        return NotImplemented

    def format(self, brief=True, fmt=None):
        return f'{self._value}'


@dataclass
class Percent(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.INT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = float(self._value.replace("%", ""))/100

    def format(self, brief=True, fmt=None):
        return '' if self._value is None else f'{self._value*100} %'


@dataclass
class Str(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.STR if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme

    def format(self, brief=True, fmt=None):
        if self._value is None:
            if self.token._value is not None:
                return self.token._value
            elif self.token.lexeme is not None:
                return self.token.lexeme
        return self._value


def _parse_bool_value(lex):
    lex = lex.lower().strip()
    return True if lex == 'true' else False
