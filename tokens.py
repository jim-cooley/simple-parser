# character class definitions:
from dataclasses import dataclass

# Token is both a Token from Parsing, as well as a 'Symbol' in the AST that is created & Symbol Table
from enum import IntEnum, auto, unique

# definitions to synchronize with statedef - note: would create circular references if left there.
CL_MAX = 37 # CL.MAX
ST_MAX = 31 # ST.MAX


@dataclass
class Token:

    @dataclass
    class Loc:
        def __init__(self, line, offset):
            self.line = 0
            self.offset = offset

    def __init__(self, tid, tcl=None, lex="", val=None, loc=None, prop=None):
        self.id: TK = tid
        self.t_class: TCL = TCL(tcl) if tcl is not None else TCL.NONE
        self.lexeme = lex
        self.value = val
        self.location = loc
        self.properties = {} if not prop else prop

    def to_string(self):
        return self.id.name

    def format(self):
        _tn = f'.{self.id.name}(' if hasattr(self.id, "name") else f'({self.id}, '
        _tcl = f'{self.t_class.name}' if hasattr(self.t_class, "name") else 'TCL({self.t_type})'
        _tv = 'None' if self.value is None else  f'{self.value}'
        _tl = f'\'{self.lexeme}\''
        _tloc = f'line:{self.location.line+1}, pos:{self.location.offset-1}'
        return f'TK{_tn}{_tcl}, {_tl}, V={_tv})'

    def map(self, tk_map):
        if self.id in tk_map:
            self.id = tk_map[self.id]
        return self


    @staticmethod
    def format_token(tk):
        return tk.format()

    @staticmethod
    def format_tid(tk):
        return f'TK.{tk.name}' if hasattr(tk, "name") else f'TK({tk})'

    @staticmethod
    def format_tt(tt):
        return f'TT.{tt.name}' if hasattr(tt, "name") else f'TT({tt})'

    # return True if two tokens are equal.  DOES NOT compare properties. Ignores unique ID
    def is_equal(self, other):
        if type(other) == type(self):
            if other.t_class == self.t_class:
                if other.value == self.value:
                    return True
        return False


# token class or category
@unique
class TCL(IntEnum):
    NONE = 0
    BINOP = auto()
    DICT = auto()   # k-v pairs
    KEYWORD = auto()
    LIST = auto()   # ordered
    LITERAL = auto()
    LOGICAL = auto()
    IDENTIFIER = auto()
    METHOD = auto()
    SERIES = auto() # dataset, panda
    SET = auto()    # unordered, set operations
    UNARY = auto()
    WHITE = auto()
    ERROR = auto()


# tokens
@unique
class TK(IntEnum):
    WHT = (ST_MAX + 1)  # 32    - numbers only provided to facilitate debugging.
    IDNT = auto()   # 33
    INT = auto()    # 34
    FLOT = auto()   # 35
    STR = auto()    # 36
    USCR = auto()   # 37
    SEMI = auto()   # 38
    COMA = auto()   # 39
    DOT = auto()    # 40
    COLN = auto()   # 41
    MNUS = auto()   # 42
    PLUS = auto()   # 43
    STAR = auto()   # 44
    SLSH = auto()   # 45
    BSLH = auto()   # 46
    PCT = auto()    # 47
    EXPN = auto()   # 48
    EQLS = auto()   # 49
    LBS = auto()    # 50
    QUOT = auto()   # 51
    EXCL = auto()   # 52
    QSTN = auto()   # 53
    AMPS = auto()   # 54
    DLRS = auto()   # 55
    ATS = auto()    # 56
    BAR = auto()    # 57
    GTR = auto()    # 58
    LESS = auto()   # 59
    LBRC = auto()   # 60
    RBRC = auto()   # 61
    LPRN = auto()   # 62
    RPRN = auto()   # 63
    LBRK = auto()   # 64
    RBRK = auto()   # 65
    TLDE = auto()   # 66
    RBAR = auto()  # >| 67
    LBAR = auto()  # <| 68
    GTR2 = auto()  # >> 69
    GTE = auto()   # >= 70
    LSS2 = auto()  # << 71
    LTE = auto()   # <= 72
    NEQ = auto()   # != 73
    EQEQ = auto()  # == 74
    BAR2 = auto()  # || 75
    AMP2 = auto()  # && 76
    TIME = auto()  # h:m:s  77
    DUR = auto()   # 1s, 1m, 1d, 1w, 1m, 1y 78

    # specialized tokens:
    INVALID = 124
    BAD = 125       # from lexer
    ERR = 126
    EOF = 127

    # the length of tokens up to here is fixed at 4 chars.  its a pain, but otherwise the state table is unmaintainable.

    RESERVED = 149  # last reserved token value (below 128 can be used in state machine, 128-255 error & reserved)

    # mathmatical operators
    ADD = auto()     # +
    SUB = auto()     # - (subtract)
    NEG = auto()     # unary - (negate)
    MUL = auto()     # *
    DIV = auto()     # /
    POW = auto()     # ^
    ISEQ = auto()    # ==
    ASSIGN = auto()  # =
    APPLY = auto()   # >>
    FALL_BELOW = auto()  # <|
    RISE_ABOVE = auto()  # >|
    PARAMETER_LIST = auto() # parameter-list
    SET = auto()
    PIPE = auto()

    # logical operators
    ALL = auto()    # all:
    ANY = auto()    # any:
    NONEOF = auto() # none:
    IN = auto()
    AND = auto()
    OR = auto()
    NONE = auto()
    NOT = auto()
    TRUE = auto()
    FALSE = auto()

    # keywords, reserved words, intrinsics
    BUY = auto()
    SELL = auto()
    SIGNAL = auto()

    LAST = 299  # last reserved token id


