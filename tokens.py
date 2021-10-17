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

    def _map(self, tk_map):
        if self.id in tk_map:
            self.id = tk_map[self.id]
        return self

    def map2binop(self):
        return self._map(_tk2binop)

    def map2unop(self):
        return self._map(_tk2unop)

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
    IDNT = auto()   #
    INT = auto()    #
    FLOT = auto()   #
    STR = auto()    #
    USCR = auto()   # _
    SEMI = auto()   # ;
    COMA = auto()   # ,
    DOT = auto()    # .
    COLN = auto()   # :
    CLN2 = auto()   # ::
    CCEQ = auto()   # :=
    CCMN = auto()   # :-
    MNUS = auto()   # -
    PLUS = auto()   # +
    STAR = auto()   # *
    SLSH = auto()   # /
    BSLH = auto()   # \
    PCT = auto()    # %
    EXPN = auto()   # ^
    EQLS = auto()   # =
    LBS = auto()    # #
    QUOT = auto()   # ", '
    EXCL = auto()   # !
    QSTN = auto()   # ?
    AMPS = auto()   # &
    DLRS = auto()   # $
    ATS = auto()    # @
    BAR = auto()    # |
    BAR2 = auto()   # ||
    GTR = auto()    # >
    LESS = auto()   # <
    LBRC = auto()   # {
    RBRC = auto()   # }
    LPRN = auto()   # (
    RPRN = auto()   # )
    LBRK = auto()   # [
    RBRK = auto()   # ]
    TLDE = auto()   # ~
    RBAR = auto()  # >|
    LBAR = auto()  # <|
    GTR2 = auto()  # >>
    GTE = auto()   # >=
    EQGT = auto()  # =>
    RARR = auto()  # ->
    LARR = auto()  # <-
    LSS2 = auto()  # <<
    LTE = auto()   # <=
    NEQ = auto()   # !=
    EQEQ = auto()  # ==
    AMP2 = auto()  # &&
    TIME = auto()  # h:m:s
    DUR = auto()   # 1s, 1m, 1d, 1w, 1m, 1y

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
    RAISE = auto()   # =>
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


# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.BAR: TK.PIPE,
    TK.STAR: TK.MUL,
    TK.SLSH: TK.DIV,
    TK.PLUS: TK.ADD,
    TK.MNUS: TK.SUB,
    TK.EQLS: TK.ASSIGN,
    TK.GTR2: TK.APPLY,
    TK.LSS2: TK.LSS2,
    TK.LBAR: TK.FALL_BELOW,
    TK.RBAR: TK.RISE_ABOVE,
    TK.AMPS: TK.AND,
    TK.EXPN: TK.POW,
    TK.COLN: TK.COLN,
    TK.EXCL: TK.NOT,
    TK.AND: TK.AND,
    TK.OR: TK.OR,
    TK.DOT: TK.DOT,
    TK.LTE: TK.LTE,
    TK.GTE: TK.GTE,
    TK.EQGT: TK.RAISE,
    TK.LESS: TK.LESS,
    TK.GTR: TK.GTR,
    TK.NEQ: TK.NEQ,
    TK.EQEQ: TK.ISEQ,  # ==
}
_tk2unop = {
    TK.PLUS: TK.PLUS,  # unary +
    TK.MNUS: TK.NEG,  # unary -
    TK.NOT: TK.NOT,
    TK.EXCL: TK.NOT,  # !
}

# token sets for the parser
_ADDITION_TOKENS = [TK.PLUS, TK.MNUS]
_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR]
_FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.EQGT]
_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ]
_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2]
_MULTIPLICATION_TOKENS = [TK.SLSH, TK.STAR, TK.EXPN, TK.DOT]
_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL]
_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.SERIES, TCL.IDENTIFIER]