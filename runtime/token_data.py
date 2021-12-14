from runtime.token_class import TCL
from runtime.token_ids import TK


# token type mapping: NOTE: this is generated data from Token, see instructions below.
_tk2type = {
    TK.ADD: TCL.BINOP,
    TK.ALL: TCL.UNARY,
    TK.AND: TCL.BINOP,
    TK.ANON: TCL.IDENTIFIER,
    TK.ANY: TCL.UNARY,
    TK.APPLY: TCL.UNARY,
    TK.ASSIGN: TCL.BINOP,
    TK.BLOCK: TCL.SCOPE,
    TK.BOOL: TCL.LITERAL,
    TK.CATEGORY: TCL.LITERAL,
    TK.CHAIN: TCL.BINOP,
    TK.COEQ: TCL.BINOP,  # not in Token
    TK.COLN: TCL.BINOP,
    TK.COMBINE: TCL.BINOP,
    TK.COMMAND: TCL.UNARY,
    TK.DATAFRAME: TCL.LITERAL,
    TK.DECREMENT: TCL.UNARY,
    TK.DEF: TCL.IDENTIFIER,
    TK.DEFINE: TCL.BINOP,
    TK.DICT: TCL.LITERAL,
    TK.DIV: TCL.BINOP,
    TK.DLRS: TCL.UNARY,
    TK.DOT: TCL.BINOP,
    TK.DUR: TCL.LITERAL,
    TK.ELSE: TCL.BINOP,
    TK.EMPTY: TCL.LITERAL,
    TK.ENUM: TCL.LITERAL,
    TK.EOF: TCL.LITERAL,
    TK.EQGT: TCL.BINOP,  # not in Token
    TK.EQLS: TCL.BINOP,  # not in Token
    TK.FALL_BELOW: TCL.BINOP,
    TK.FLOT: TCL.LITERAL,
    TK.FUNCTION: TCL.FUNCTION,
    TK.GEN: TCL.FUNCTION,
    TK.GTE: TCL.BINOP,
    TK.GTR: TCL.BINOP,
    TK.IDENT: TCL.IDENTIFIER,
    TK.IDIV: TCL.BINOP,
    TK.IF: TCL.BINOP,
    TK.IN: TCL.BINOP,
    TK.INCREMENT: TCL.UNARY,
    TK.INDEX: TCL.BINOP,
    TK.INT: TCL.LITERAL,
    TK.ISEQ: TCL.BINOP,
    TK.KVPAIR: TCL.BINOP,   # not in Token
    TK.LESS: TCL.BINOP,
    TK.LIST: TCL.LITERAL,
    TK.LTE: TCL.BINOP,
    TK.MNEQ: TCL.BINOP,
    TK.MOD: TCL.BINOP,
    TK.MUL: TCL.BINOP,
    TK.NAMEDTUPLE: TCL.TUPLE,
    TK.NEG: TCL.UNARY,
    TK.NEQ: TCL.BINOP,
    TK.NONE: TCL.LITERAL,
    TK.NONEOF: TCL.UNARY,
    TK.NOT: TCL.UNARY,
    TK.NOW: TCL.FUNCTION,
    TK.OBJECT: TCL.LITERAL,
    TK.OR: TCL.BINOP,
    TK.PAPPLY: TCL.BINOP,
    TK.PCT: TCL.UNARY,
    TK.PLEQ: TCL.BINOP,
    TK.POS: TCL.UNARY,
    TK.POW: TCL.BINOP,
    TK.PUT: TCL.BINOP,
    TK.PRODUCE: TCL.BINOP,
    TK.PROPCALL: TCL.BINOP,
    TK.RAISE: TCL.UNARY,
    TK.RANGE: TCL.BINOP,
    TK.REF: TCL.BINOP,
    TK.RETURN: TCL.UNARY,
    TK.RISE_ABOVE: TCL.BINOP,
    TK.SERIES: TCL.LITERAL,
    TK.SET: TCL.LITERAL,
    TK.STR: TCL.LITERAL,
    TK.SLICE: TCL.BINOP,
    TK.SUB: TCL.BINOP,
    TK.SUBSCRIPT: TCL.BINOP,
    TK.THEN: TCL.BINOP,
    TK.TIME: TCL.LITERAL,
    TK.TODAY: TCL.FUNCTION,
    TK.TUPLE: TCL.TUPLE,
    TK.VAL: TCL.UNARY,
    TK.VAR: TCL.UNARY,
    TK.WHT: TCL.NONE,
}
# token to glyph.  NOTE: soon to be generated data
_tk2glyph = {
    TK.ADD: '+',  # +
    TK.ALL: 'all',  # all:
    TK.AND: 'and',
    TK.ANY: 'any',  # any:
    TK.APPLY: 'apply',  # >>
    TK.ASSIGN: '=',  # =
    TK.CATEGORY: 'cat',
    TK.CHAIN: '|',
    TK.COEQ: ':=',
    TK.COLN: ':',
    TK.COMBINE: ':',
    TK.COMMAND: 'command',
    TK.COMPARE: '?',
    TK.DATAFRAME: 'dataframe',
    TK.DECREMENT: '--',
    TK.DEFINE: ':=',
    TK.DEFINE_FN: '=>',
    TK.DICT: 'dict',
    TK.DIV: '/',
    TK.DOT: '.',
    TK.DUR: 'dur',
    TK.EMPTY: 'Ø',  # empty set
    TK.ENUM: 'enum',
    TK.EQLS: '=',
    TK.EQGT: '=>',
    TK.EVENT: '=>',
    TK.FALL_BELOW: '<|',
    TK.FALSE: 'false',
    #   TK.FUNCTION: 'fn',
    TK.GEN: 'gen',
    TK.GTE: '>=',
    TK.GTR: '>',
    TK.IDIV: 'div',
    TK.IF: 'if',
    TK.IN: 'in',
    TK.INDEX: 'index',   # indexing expression
    TK.INCREMENT: '++',
    TK.SUBSCRIPT: '[]',
    TK.INT: 'i',
    TK.ISEQ: '==',
    TK.KVPAIR: ':',
    TK.LIST: 'list',
    TK.LESS: '<',
    TK.LTE: '<=',
    TK.MNEQ: '-=',
    TK.MUL: '*',
    TK.NAMEDTUPLE: 'ntup',
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
    TK.PUT: 'put',
    TK.PUTIDX: 'iput',
    TK.PRODUCE: '=>',
    TK.PROPCALL: 'pcall',
    TK.RANGE: 'range',
    TK.RBRC: '}',
    TK.REF: 'ref',
    TK.RETURN: 'ret',
    TK.RISE_ABOVE: '|>',  # >|`
    TK.SERIES: 'series',
    TK.SET: 'set',
    TK.SLICE: 'slice',
    TK.STR: 'str',
    TK.SUB: '-',  # - (subtract)
    TK.TODAY: 'today',
    TK.TRUE: 'true',
    TK.TUPLE: 'tup',
    TK.VAL: 'val',
    TK.VAR: 'var',
}

# UNDONE: remove the need for _tk2binop and _tk2unop by just using the mapped token.  There may be places this is not
# possible, ie: TK.MNUS maps to TK.NEG (unary), or TK.SUB (binary) depending on context. But these are the things that
# should be left after just using the correct tokens in the lexer for all others.
_tk2binop = {
    TK.AMPS: TK.AND,
    TK.AND: TK.AND,
    TK.BAR: TK.CHAIN,
    TK.CLN2: TK.DEF,
    TK.COEQ: TK.DEFINE,
    TK.COLN: TK.COMBINE,  # TK.KVPAIR ? TK.PARAMETERIZE, TK.PARAMETER_APPLY
    TK.COMBINE: TK.COMBINE,
    TK.DOT2: TK.RANGE,
    TK.DOT: TK.DOT,
    TK.EQEQ: TK.ISEQ,  # ==
    TK.EQGT: TK.PRODUCE,
    TK.EQLS: TK.ASSIGN,  # or TK.DEFINE
    TK.EXCL: TK.NOT,
    TK.EXPN: TK.POW,
    TK.GTE: TK.GTE,
    TK.GTR2: TK.APPLY,
    TK.GTR: TK.GTR,
    TK.IDIV: TK.IDIV,
    TK.IN: TK.IN,
    TK.IF: TK.IF,
    TK.LBAR: TK.FALL_BELOW,
    TK.LBRK: TK.INDEX,
    TK.LESS: TK.LESS,
    TK.LSS2: TK.LSS2,
    TK.LTE: TK.LTE,
    TK.MNUS: TK.SUB,
    TK.MOD: TK.MOD,
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
    TK.MNU2: TK.DECREMENT,  # unary --
    TK.NONE: TK.NONEOF,
    TK.NOT: TK.NOT,
    TK.PLUS: TK.POS,  # unary +
    TK.PLU2: TK.INCREMENT,  # unary ++
    TK.RETURN: TK.RETURN,
    TK.VAL: TK.VAL,
    TK.VAR: TK.VAR,
}
# UNDONE: remove the need for this. by removing TK.FALSE, TK.TRUE, TK.TODAY, TK.NOW as unique tokens and just use
# the type token with a constant value (see Token.FALSE, for instance)
_tk2lit = {
    TK.BOOL: TK.BOOL,
    TK.DUR: TK.DUR,
    TK.FALSE: TK.BOOL,
    TK.FLOT: TK.FLOT,
    TK.INT: TK.INT,
    TK.LBRK: TK.LIST,  # ]
    TK.QUOT: TK.STR,
    TK.STR: TK.STR,
    TK.TIME: TK.TIME,
    TK.TODAY: TK.TIME,
    TK.TRUE: TK.BOOL,
}

type2tid = {
    'Block': TK.BLOCK,
    'Bool': TK.BOOL,
    'Category': TK.CATEGORY,
    'Dataset': TK.DATAFRAME,
    'DataFrame': TK.DATAFRAME,
    'dataframe': TK.DATAFRAME,
    'datetime': TK.TIME,
    'Dict': TK.DICT,
    'Enumeration': TK.ENUM,
    'List': TK.LIST,
    'NoneType': TK.NONE,
    'Object': TK.OBJECT,
    'Range': TK.RANGE,
    'Series': TK.SERIES,
    'series': TK.SERIES,
    'bool': TK.BOOL,
    'dict': TK.DICT,
    'float': TK.FLOT,
    'int': TK.INT,
    'list': TK.LIST,
    'object': TK.NONE,  # CONSIDER: TK.OBJECT ?
    'range': TK.RANGE,
    'Set': TK.SET,
    'str': TK.STR,
    'timedelta': TK.DUR,
}

# maps extended special characters directly to tokens
u16_to_tkid = {
    '•': TK.DOTPROD,
    'Ø': TK.EMPTY,
}

# token sets for the parser
ASSIGNMENT_TOKENS = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.GTR2, TK.MNEQ, TK.PLEQ]
ASSIGNMENT_TOKENS_EX = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.MNEQ, TK.PLEQ, TK.COLN]
ASSIGNMENT_TOKENS_REF = [TK.COEQ, TK.EQLS, TK.EQGT, TK.ASSIGN, TK.COLN]
FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.APPLY, TK.RARR]

IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.DATASET, TCL.IDENTIFIER, TCL.TUPLE, TCL.FUNCTION]
IDENTIFIER_TOKENS = [TK.IDENT, TK.ANON, TK.REF, TK.DOT, TK.COMBINE, TK.FUNCTION]

# used in assignment (k=v, k:v)
IDENTIFIER_TOKENS_EX = [TK.ANON, TK.BLOCK, TK.CHAIN, TK.COLN, TK.COMBINE, TK.DOT,
                        TK.FUNCTION, TK.GEN, TK.IDENT, TK.RANGE, TK.REF, TK.TUPLE, TK.STR, TK.INDEX,
                        TK.PROPCALL]
VALUE_TOKENS = [TK.BOOL, TK.DUR, TK.EMPTY, TK.FLOT, TK.IDENT, TK.INT, TK.LIST, TK.NONE, TK.OBJECT, TK.SET, TK.STR]

ADDITION_TOKENS = [TK.PLUS, TK.MNUS, TK.SUB, TK.ADD]
COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR, TK.FALL_BELOW, TK.RISE_ABOVE]
EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ, TK.ISEQ]
LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2, TK.QSTN]
MULTIPLICATION_TOKENS = [TK.SLSH, TK.DIV, TK.STAR, TK.MUL, TK.EXPN, TK.POW, TK.DOT, TK.DOT2,
                         TK.RANGE, TK.IDIV, TK.MOD]
UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL, TK.MNU2, TK.PLU2]
SET_UNARY_TOKENS = [TK.NONE, TK.ALL, TK.ANY]

EXPRESSION_TOKENS = ADDITION_TOKENS + MULTIPLICATION_TOKENS + UNARY_TOKENS \
                    + LOGIC_TOKENS + EQUALITY_TEST_TOKENS + COMPARISON_TOKENS + SET_UNARY_TOKENS
