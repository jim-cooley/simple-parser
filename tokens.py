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
    COMMAND = auto()
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
    WHT = (ST_MAX + 1)  #
    EOL = auto()   # \n
    AMP2 = auto()  # &&
    AMPS = auto()   # &
    ATS = auto()    # @
    BAR = auto()    # |
    BAR2 = auto()   # ||
    BSLH = auto()   # \
    CCEQ = auto()   # :=
    CCMN = auto()   # :-
    CLN2 = auto()   # ::
    COLN = auto()   # :
    COMA = auto()   # ,
    DLRS = auto()   # $
    DOT = auto()    # .
    DOT2 = auto()   # ..
    DUR = auto()   # 1s, 1m, 1d, 1w, 1m, 1y
    EQEQ = auto()  # ==
    EQGT = auto()  # =>
    EQLS = auto()   # =
    EXCL = auto()   # !
    EXPN = auto()   # ^
    FLOT = auto()   #
    GTE = auto()   # >=
    GTR = auto()    # >
    GTR2 = auto()  # >>
    IDNT = auto()   #
    INT = auto()    #
    LARR = auto()  # <-
    LBAR = auto()  # <|
    LBRC = auto()   # {
    LBRK = auto()   # [
    LBS = auto()    # #
    LESS = auto()   # <
    LPRN = auto()   # (
    LSS2 = auto()  # <<
    LTE = auto()   # <=
    MNEQ = auto()   # -=
    MNU2 = auto()   # --
    MNUS = auto()   # -
    NEQ = auto()   # !=
    PCT = auto()    # %
    PCT2 = auto()   # %
    PLEQ = auto()   # +=
    PLU2 = auto()   # ++
    PLUS = auto()   # +
    QSTN = auto()   # ?
    QUOT = auto()   # ", '
    RARR = auto()  # ->
    RBAR = auto()  # >|
    RBRC = auto()   # }
    RBRK = auto()   # ]
    RPRN = auto()   # )
    SEMI = auto()   # ;
    SLSH = auto()   # /
    STAR = auto()   # *
    STR = auto()    #
    TIME = auto()  # h:m:s
    TLDE = auto()   # ~
    USCR = auto()   # _

    # specialized tokens:
    INVALID = 124
    BAD = 125       # from lexer
    ERR = 126
    EOF = 127

    # the length of tokens up to here is fixed at 4 chars.  its a pain, but otherwise the state table is unmaintainable.

    RESERVED = 149  # last reserved token value (below 128 can be used in state machine, 128-255 error & reserved)

    # higher-level / derived tokens
    ADD = auto()     # +
    ALL = auto()    # all:
    AND = auto()
    ANY = auto()    # any:
    APPLY = auto()   # >>
    ASSIGN = auto()  # =
    DIV = auto()     # /
    EVENT = auto()   # from =>
    FALL_BELOW = auto()  # <|
    FALSE = auto()
    IN = auto()
    ISEQ = auto()    # ==
    MUL = auto()     # *
    NEG = auto()     # unary - (negate)
    NONE = auto()
    NONEOF = auto() # none:
    NOT = auto()
    OR = auto()
    PARAMETER_LIST = auto() # parameter-list
    PIPE = auto()
    POW = auto()     # ^
    RAISE = auto()   # =>
    RISE_ABOVE = auto()  # >|
    SET = auto()
    SUB = auto()     # - (subtract)
    TRUE = auto()

    # keywords, reserved words, intrinsics
    BUY = auto()
    SELL = auto()
    SIGNAL = auto()
    DEFINE = auto()
    COMMAND = auto()

    LAST = 299  # last reserved token id


# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.AMPS: TK.AND,
    TK.AND: TK.AND,
    TK.BAR: TK.PIPE,
    TK.CCEQ: TK.DEFINE,
    TK.CLN2: TK.EVENT,
    TK.COLN: TK.COLN,
    TK.DOT: TK.DOT,
    TK.EQEQ: TK.ISEQ,  # ==
    TK.EQGT: TK.RAISE,
    TK.EQLS: TK.ASSIGN,
    TK.EXCL: TK.NOT,
    TK.EXPN: TK.POW,
    TK.GTE: TK.GTE,
    TK.GTR2: TK.APPLY,
    TK.GTR: TK.GTR,
    TK.LBAR: TK.FALL_BELOW,
    TK.LESS: TK.LESS,
    TK.LSS2: TK.LSS2,
    TK.LTE: TK.LTE,
    TK.MNUS: TK.SUB,
    TK.NEQ: TK.NEQ,
    TK.OR: TK.OR,
    TK.PCT: TK.PCT,
    TK.PCT2: TK.COMMAND,
    TK.PLUS: TK.ADD,
    TK.RBAR: TK.RISE_ABOVE,
    TK.SLSH: TK.DIV,
    TK.STAR: TK.MUL,
}
_tk2unop = {
    TK.EXCL: TK.NOT,  # !
    TK.MNUS: TK.NEG,  # unary -
    TK.NOT: TK.NOT,
    TK.PLUS: TK.PLUS,  # unary +
}

# token sets for the parser
_ADDITION_TOKENS = [TK.PLUS, TK.MNUS, TK.MNEQ, TK.PLEQ]
_ASSIGNMENT_TOKENS = [TK.EQLS, TK.ASSIGN, TK.CCEQ]
_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR]
_FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.EQGT, TK.PCT2]
_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ]
_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2]
_MULTIPLICATION_TOKENS = [TK.SLSH, TK.STAR, TK.EXPN, TK.DOT, TK.DOT2]
_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL, TK.MNU2, TK.PLU2]
_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.SERIES, TCL.IDENTIFIER]