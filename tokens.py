# character class definitions:
from dataclasses import dataclass

# Token is both a Token from Parsing, as well as a 'Symbol' in the AST that is created & Symbol Table
from enum import IntEnum, auto, unique

# definitions to synchronize with statedef - note: would create circular references if left there.
CL_MAX = 37  # CL.MAX
ST_MAX = 31  # ST.MAX


# token class or category
@unique
class TCL(IntEnum):
    NONE = 0
    BINOP = auto()
    COMMAND = auto()
    DATASET = auto()  # dataset, panda
    DICT = auto()  # k-v pairs
    FUNCTION = auto()
    KEYWORD = auto()
    LIST = auto()  # ordered
    LITERAL = auto()
    LOGICAL = auto()
    IDENTIFIER = auto()
    SET = auto()  # unordered, set operations
    UNARY = auto()
    WHITE = auto()
    ERROR = auto()


# tokens
@unique
class TK(IntEnum):
    # the first section are lexemes from the state table.
    # higher-level, derived tokens are next
    # do not mix the two as these must be < 127 in value (including error states)
    WHT = (ST_MAX + 1)  #
    EOL = auto()  # \n
    AMP2 = auto()  # &&
    AMPS = auto()  # &
    ATS = auto()  # @
    BAR = auto()  # |
    BAR2 = auto()  # ||
    BSLH = auto()  # \
    CLN2 = auto()  # ::
    COEQ = auto()  # :=
    COLN = auto()  # :
    COMA = auto()  # ,
    COMN = auto()  # :-
    DLRS = auto()  # $
    DOT = auto()  # .
    DOT2 = auto()  # ..
    DUR = auto()  # 1s, 1m, 1d, 1w, 1m, 1y
    EMPTY = auto() # ø empty set
    EQEQ = auto()  # ==
    EQGT = auto()  # =>
    EQLS = auto()  # =
    EXCL = auto()  # !
    EXPN = auto()  # ^
    FLOT = auto()  #
    GTE = auto()  # >=
    GTR = auto()  # >
    GTR2 = auto()  # >>
    IDNT = auto()  #
    INT = auto()  #
    LARR = auto()  # <-
    LBAR = auto()  # <|
    LBRC = auto()  # {
    LBRK = auto()  # [
    LBS = auto()  # #
    LESS = auto()  # <
    LPRN = auto()  # (
    LSS2 = auto()  # <<
    LTE = auto()  # <=
    MNEQ = auto()  # -=
    MNU2 = auto()  # --
    MNUS = auto()  # -
    NEQ = auto()  # !=
    PCT = auto()  # %
    PCT2 = auto()  # %
    PLEQ = auto()  # +=
    PLU2 = auto()  # ++
    PLUS = auto()  # +
    QSTN = auto()  # ?
    QUOT = auto()  # ", '
    RARR = auto()  # ->
    RBAR = auto()  # >|
    RBRC = auto()  # }
    RBRK = auto()  # ]
    RPRN = auto()  # )
    SEMI = auto()  # ;
    SLSH = auto()  # /
    STAR = auto()  # *
    STR = auto()  #
    TIME = auto()  # h:m:s
    TLDE = auto()  # ~
    USCR = auto()  # _
    #
    SPEC = auto()  # special character tokens
    LATX = auto()  # LaTeX supported escape codes %code vs \code{}
    HTML_ESCAPE = auto()  # Html-style escape code: &ne vs &ne;
    UNICODE = auto()  # \u...

    #
    # specialized tokens (error states):
    EOF = 127
    ERR = auto()
    BAD = auto()
    INVALID = auto()

    #
    # the length of tokens up to here is fixed at 4 chars.  its a pain, but otherwise the state table is unmaintainable.

    RESERVED = 200
    # last reserved token value (below 128 can be used in state machine, 128-255 error & reserved)
    #

    #
    # higher-level / derived tokens
    #
    ADD = auto()  # +
    ALL = auto()  # all:
    AND = auto()
    ANY = auto()  # any:
    APPLY = auto()  # >>
    ASSIGN = auto()  # =
    BOOL = auto()
    BUY = auto()
    COMMAND = auto()
    COMPARE = auto()    # ?  a ? b is to compare a to b
    DECREMENT = auto()  # --
    DEFINE = auto()     # :=
    DEFATTR = auto()    # 'def' <ident> =
    DIV = auto()  # /
    DOTPROD = auto() # •
    EVENT = auto()  # from =>
    FALL_BELOW = auto()  # <|
    FALSE = auto()
    FUNCTION = auto()
    IN = auto()
    INCREMENT = auto()
    INDEX = auto()  # indexing expression
    ISEQ = auto()  # ==
    LIST = auto()
    MOD = auto()
    MUL = auto()  # *
    NEG = auto()  # unary - (negate)
    NONE = auto()
    NONEOF = auto()  # none:
    NOT = auto()
    NOW = auto()
    OR = auto()
    PARAMETER_LIST = auto()  # parameter-list
    PIPE = auto()
    POS = auto()  # unary +
    POW = auto()  # ^
    RAISE = auto()  # =>
    RANGE = auto()
    REF = auto()
    RISE_ABOVE = auto()  # >|
    SELL = auto()
    SET = auto()
    SIGNAL = auto()
    SUB = auto()  # - (subtract)
    TODAY = auto()
    TRUE = auto()
    TUPLE = auto()
    VAR = auto()

    LAST = 299  # last reserved token id


# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.AMPS: TK.AND,
    TK.AND: TK.AND,
    TK.BAR: TK.PIPE,
    TK.CLN2: TK.EVENT,
    TK.COEQ: TK.DEFINE,
    TK.COLN: TK.TUPLE,
    TK.DOT2: TK.RANGE,
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
    TK.LBRK: TK.INDEX,
    TK.LESS: TK.LESS,
    TK.LSS2: TK.LSS2,
    TK.LTE: TK.LTE,
    TK.MNUS: TK.SUB,
    TK.NEQ: TK.NEQ,
    TK.OR: TK.OR,
    TK.PCT2: TK.COMMAND,
    TK.PCT: TK.PCT,
    TK.PLUS: TK.ADD,
    TK.QSTN: TK.COMPARE,
    TK.RARR: TK.RAISE,
    TK.RBAR: TK.RISE_ABOVE,
    TK.SLSH: TK.DIV,
    TK.STAR: TK.MUL,
}
_tk2unop = {
    TK.EXCL: TK.NOT,  # !
    TK.MNUS: TK.NEG,  # unary -
    TK.MNU2: TK.DECREMENT, # unary --
    TK.NOT: TK.NOT,
    TK.PLUS: TK.POS,  # unary +
    TK.PLU2: TK.INCREMENT, # unary ++
}
_tk2lit = {
    TK.LBRK: TK.LIST,  # ]
    TK.QUOT: TK.STR,
}
# token type mapping
_tk2type = {
    TK.DLRS: TCL.UNARY,
    TK.DUR: TCL.LITERAL,
    TK.EQLS: TCL.BINOP,
    TK.EXCL: TCL.LOGICAL,
    TK.EXPN: TCL.BINOP,
    TK.FLOT: TCL.LITERAL,
    TK.GTE: TCL.LOGICAL,
    TK.GTR: TCL.LOGICAL,
    TK.INT: TCL.LITERAL,
    TK.LBAR: TCL.BINOP,
    TK.LESS: TCL.LOGICAL,
    TK.LTE: TCL.LOGICAL,
    TK.MNU2: TCL.UNARY,
    TK.MNUS: TCL.UNARY,
    TK.NEQ: TCL.LOGICAL,
    TK.NOW: TCL.FUNCTION,
    TK.PCT: TCL.UNARY,
    TK.PLUS: TCL.UNARY,
    TK.RBAR: TCL.BINOP,
    TK.SLSH: TCL.BINOP,
    TK.STAR: TCL.BINOP,
    TK.STR: TCL.LITERAL,
    TK.TODAY: TCL.FUNCTION,
    TK.TIME: TCL.LITERAL,
    TK.VAR: TCL.UNARY,
    TK.WHT: TCL.NONE,
}
# maps extended special characters directly to tokens
u16_to_tkid = {
    '•': TK.DOTPROD,
    'Ø': TK.EMPTY,
}

# token sets for the parser
_ADDITION_TOKENS = [TK.PLUS, TK.MNUS]
_ASSIGNMENT_TOKENS = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.MNEQ, TK.PLEQ]
_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR]
_FLOW_TOKENS = [TK.BAR, TK.EQGT, TK.GTR2, TK.RARR]
_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ]
_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2, TK.QSTN]
_MULTIPLICATION_TOKENS = [TK.SLSH, TK.STAR, TK.EXPN, TK.DOT, TK.DOT2]
_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL, TK.MNU2, TK.PLU2]
_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.DATASET, TCL.IDENTIFIER]


@dataclass
class Token:
    @dataclass
    class Loc:
        def __init__(self, line=0, offset=0):
            self.line = line
            self.offset = offset

    def __init__(self, tid, tcl=None, lex="", val=None, loc=None, prop=None):
        self.id: TK = tid
        self.t_class: TCL = TCL(tcl) if tcl is not None else TCL.NONE
        self.lexeme = lex
        self.value = val
        self.location = loc
        self.properties = {} if not prop else prop

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

    def to_string(self):
        return self.id.name

    def format(self):
        _tn = f'.{self.id.name}(' if hasattr(self.id, "name") else f'({self.id}, '
        _tcl = f'{self.t_class.name}' if hasattr(self.t_class, "name") else 'TCL({self.t_type})'
        _tv = 'None' if self.value is None else f'{self.value}'
        _tl = f'\'{self.lexeme}\''
        if _tl == '\'\n\'':
            _tl = "'\\n'"
        if self.properties is not None and len(self.properties.keys()) > 0:
            _props = f': {self.properties}'
        else:
            _props = ''
#       _tloc = f'line:{self.location.line + 1}, pos:{self.location.offset - 1}'
        return f'TK{_tn}{_tcl}, {_tl}, V={_tv}){_props}'

    def _map(self, tk_map):
        if self.id in tk_map:
            self.id = tk_map[self.id]
        return self

    def _map_cl(self, tcl_map):
        if self.id in tcl_map:
            self.t_class = tcl_map[self.id]
        return self

    def map2binop(self):
        return self._map(_tk2binop)

    def map2unop(self):
        return self._map(_tk2unop)

    def map2litval(self):
        return self._map(_tk2lit)

    def map2tclass(self):
        return self._map_cl(_tk2type)

    @staticmethod
    def format_token(tk):
        return tk.format()

    @staticmethod
    def format_tid(tk):
        return f'TK.{tk.name}' if hasattr(tk, "name") else f'TK({tk})'

    @staticmethod
    def format_tt(tt):
        return f'TT.{tt.name}' if hasattr(tt, "name") else f'TT({tt})'
