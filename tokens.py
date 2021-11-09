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
    DATASET = auto()  # dataset, panda
    FUNCTION = auto()
    KEYWORD = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    SCOPE = auto()
    TUPLE = auto()
    UNARY = auto()
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
    ASSIGN = auto()  # =
    BLOCK = auto()
    BOOL = auto()
    CHAIN = auto()
    COMMAND = auto()
    COMPARE = auto()    # ?  a ? b is to compare a to b
    DECREMENT = auto()  # --
    DEF = auto()     # set version of REF
    DEFINE = auto()     # :=, 'def'
    DEFINE_FN = auto()     # =>,  'def' f(x)
    DOTPROD = auto()  # •
    EVENT = auto()  # from =>
    FALL_BELOW = auto()  # <|
    FUNCTION = auto()
    IDIV = auto()   # integer division
    INCREMENT = auto()
    INDEX = auto()  # indexing expression
    ISEQ = auto()  # ==
    KVPAIR = auto()  # key:value
    LIST = auto()
    MUL = auto()  # *
    NATIVE = auto()    # token represents native literal
    NEG = auto()  # unary - (negate)
    OBJECT = auto()  # unknown type
    OR = auto()
    POS = auto()  # unary +
    POW = auto()  # ^
    PRODUCE = auto()  # => signal
    RAISE = auto()  # ->
    REF = auto()
    RISE_ABOVE = auto()  # >|
    SET = auto()
    SUB = auto()  # - (subtract)
    TUPLE = auto()

    LAST = 299  # last reserved token id

    # keywords & intrinsic functions
    ALL = auto()   # all:
    AND = auto()
    ANON = auto()  # anonymous parameter '_'
    ANY = auto()   # any:
    APPLY = auto()  # >>
    BUY = auto()
    DATAFRAME = auto()
    DIV = auto()  # /
    EMPTY = auto()  # ø empty set
    FALSE = auto()
    IN = auto()
    MOD = auto()
    NONE = auto()
    NONEOF = auto()  # none:
    NOT = auto()
    NOW = auto()
    RANGE = auto()
    SELL = auto()
    SIGNAL = auto()
    TODAY = auto()
    TRUE = auto()
    VAR = auto()


# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.AMPS: TK.AND,
    TK.AND: TK.AND,
    TK.BAR: TK.CHAIN,
    TK.CLN2: TK.DEF,
    TK.COEQ: TK.DEFINE,
    TK.COLN: TK.KVPAIR,
    TK.DOT2: TK.RANGE,
    TK.DOT: TK.DOT,
    TK.EQEQ: TK.ISEQ,  # ==
    TK.EQGT: TK.PRODUCE,
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
    TK.ALL: TK.ALL,
    TK.ANY: TK.ANY,
    TK.EXCL: TK.NOT,  # !
    TK.MNUS: TK.NEG,  # unary -
    TK.MNU2: TK.DECREMENT, # unary --
    TK.NONE: TK.NONEOF,
    TK.NOT: TK.NOT,
    TK.PLUS: TK.POS,  # unary +
    TK.PLU2: TK.INCREMENT, # unary ++
}
_tk2lit = {
    TK.BOOL: TK.BOOL,
    TK.DUR: TK.DUR,
    TK.FLOT: TK.FLOT,
    TK.INT: TK.INT,
    TK.LBRK: TK.LIST,  # ]
    TK.QUOT: TK.STR,
    TK.STR: TK.STR,
    TK.TIME: TK.TIME,
    TK.TODAY: TK.TIME,
}
# token type mapping
_tk2type = {
    TK.DEF: TCL.IDENTIFIER,
    TK.DLRS: TCL.UNARY,
    TK.DUR: TCL.LITERAL,
    TK.EQLS: TCL.BINOP,
    TK.EXCL: TCL.BINOP,
    TK.EXPN: TCL.BINOP,
    TK.FLOT: TCL.LITERAL,
    TK.GTE: TCL.BINOP,
    TK.GTR: TCL.BINOP,
    TK.INT: TCL.LITERAL,
    TK.LBAR: TCL.BINOP,
    TK.LESS: TCL.BINOP,
    TK.LIST: TCL.TUPLE,
    TK.LTE: TCL.BINOP,
    TK.MNU2: TCL.UNARY,
    TK.MNUS: TCL.UNARY,
    TK.NEQ: TCL.BINOP,
    TK.NOW: TCL.FUNCTION,
    TK.OBJECT: TCL.LITERAL,
    TK.PCT: TCL.UNARY,
    TK.PLUS: TCL.UNARY,
    TK.RBAR: TCL.BINOP,
    TK.REF: TCL.IDENTIFIER,
    TK.SLSH: TCL.BINOP,
    TK.STAR: TCL.BINOP,
    TK.STR: TCL.LITERAL,
    TK.TIME: TCL.LITERAL,
    TK.TODAY: TCL.FUNCTION,
    TK.TUPLE: TCL.TUPLE,
    TK.VAR: TCL.UNARY,
    TK.WHT: TCL.NONE,
}
# token to glyph
_tk2glyph = {
    TK.ADD: '+',  # +
    TK.ALL: 'all',  # all:
    TK.AND: 'and',
    TK.ANY: 'any',  # any:
    TK.APPLY: 'apply',  # >>
    TK.ASSIGN: '=',  # =
    TK.BUY: 'buy',
    TK.CHAIN: '|',
    TK.COEQ: ':=',
    TK.COLN: ':',
    TK.COMMAND: 'command',
    TK.COMPARE: '?',
    TK.DECREMENT: '--',
    TK.DEFINE: ':=',
    TK.DEFINE_FN: '=>',
    TK.DIV: '/',
    TK.DUR: 'dur',
    TK.EMPTY: 'Ø',  # empty set
    TK.EQLS: '=',
    TK.EQGT: '=>',
    TK.EVENT: '=>',
    TK.FALL_BELOW: '<|',
    TK.FALSE: 'false',
#   TK.FUNCTION: 'fn',
    TK.GTE: '>=',
    TK.GTR: '>',
    TK.IDIV: 'div',
    TK.IN: 'in',
    TK.INCREMENT: '++',
    TK.INDEX: '[]',  # indexing expression
    TK.INT: 'i',
    TK.ISEQ: '==',
    TK.KVPAIR: ':',
    TK.LESS: '<',
    TK.LTE: '<=',
    TK.MNEQ: '-=',
    TK.MUL: '*',
    TK.NEG: '-',
    TK.NEQ: '!=',
    TK.NONE: 'none',
    TK.NONEOF: 'noneof',  # none:
    TK.NOT: 'not',
    TK.NOW: 'now',
    TK.OR: 'or',
    TK.PCT: '%',
    TK.PLEQ: '+=',
    TK.POS: '+',
    TK.POW: '^',
    TK.PRODUCE: '=>',
    TK.RANGE: 'range',
    TK.RBRC: '}',
    TK.REF: 'ref',
    TK.RISE_ABOVE: '|>',  # >|
    TK.SELL: 'sell',
    TK.SET: 'set',
    TK.SIGNAL: 'signal',
    TK.STR: 'str',
    TK.SUB: '-',  # - (subtract)
    TK.TODAY: 'today',
    TK.TRUE: 'true',
    TK.TUPLE: '',
    TK.VAR: 'var',
}

native2tkid = {
    'bool': TK.BOOL,
    'float': TK.FLOT,
    'int':  TK.INT,
    'NoneType': TK.NONE,
    'object': TK.NONE,
    'str': TK.STR,
    'timedelta': TK.DUR,
    'Object': TK.OBJECT,
    'Block': TK.BLOCK,
}

# maps extended special characters directly to tokens
u16_to_tkid = {
    '•': TK.DOTPROD,
    'Ø': TK.EMPTY,
}

# token sets for the parser
_ADDITION_TOKENS = [TK.PLUS, TK.MNUS]
_ASSIGNMENT_TOKENS = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.GTR2, TK.MNEQ, TK.PLEQ]
_ASSIGNMENT_TOKENS_EX = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.MNEQ, TK.PLEQ, TK.COLN]
_ASSIGNMENT_TOKENS_REF = [TK.COEQ, TK.EQLS, TK.EQGT, TK.ASSIGN, TK.COLN]
_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR]
_FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.APPLY, TK.RARR]
_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ]
_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2, TK.QSTN]
_MULTIPLICATION_TOKENS = [TK.SLSH, TK.STAR, TK.EXPN, TK.DOT, TK.DOT2, TK.IDIV, TK.MOD]
_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL, TK.MNU2, TK.PLU2]
_SET_UNARY_TOKENS = [TK.NONE, TK.ALL, TK.ANY]
_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.DATASET, TCL.IDENTIFIER, TCL.TUPLE, TCL.FUNCTION]
_IDENTIFIER_TOKENS = [TK.IDNT, TK.ANON, TK.REF, TK.DOT, TK.TUPLE, TK.FUNCTION]
_IDENTIFIER_TOKENS_EX = [TK.IDNT, TK.ANON, TK.REF, TK.DOT, TK.TUPLE, TK.FUNCTION, TK.COLN, TK.BLOCK, TK.BUY, TK.SELL, TK.CHAIN]
_VALUE_TOKENS = [TK.BOOL, TK.FLOT, TK.EMPTY, TK.INT, TK.NONE, TK.STR, TK.DUR, TK.OBJECT, TK.SET, TK.LIST, TK.IDNT]


@dataclass
class Token:
    @dataclass
    class Loc:
        def __init__(self, line=0, offset=0):
            self.line = line
            self.offset = offset

    def __init__(self, tid, tcl=None, lex="", val=None, loc=None):
        self.id = tid
        self.t_class: TCL = TCL(tcl) if tcl is not None else TCL.NONE
        self.lexeme = lex
        self.value = val
        self.location = loc if loc is not None else Token.Loc()

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

    def map2unop(self):
        return self._map(_tk2unop)

    def map2litval(self):
        return self._map(_tk2lit)

    def map2tclass(self):
        return self._map_cl(_tk2type)

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
            self.id = tk_map[self.id]
        return self

    def _map_cl(self, tcl_map):
        if self.id in tcl_map:
            self.t_class = tcl_map[self.id]
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


TK_EOF = Token(TK.EOF, TCL.LITERAL, '', None)
TK_EMPTY = Token(TK.EMPTY, TCL.LITERAL, '{}', {})
TK_NONE = Token(TK.NONE, TCL.LITERAL, '', None)
TK_SET = Token(TK.SET, TCL.LITERAL, '{', None)
TK_ASSIGN = Token(TK.ASSIGN, TCL.FUNCTION)
TK_DEFINE = Token(TK.DEFINE, TCL.FUNCTION)
