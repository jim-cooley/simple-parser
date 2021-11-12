from environment.token_class import TCL
from environment.token_ids import TK


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
}
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
    TK.IF: 'if',
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
    TK.RETURN: 'ret',
    TK.RISE_ABOVE: '|>',  # >|
    TK.SELL: 'sell',
    TK.SET: 'set',
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
    'int': TK.INT,
    'NoneType': TK.NONE,
    'object': TK.NONE,  # CONSIDER: TK.OBJECT ?
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
_ASSIGNMENT_TOKENS = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.GTR2, TK.MNEQ, TK.PLEQ]
_ASSIGNMENT_TOKENS_EX = [TK.COEQ, TK.EQLS, TK.ASSIGN, TK.MNEQ, TK.PLEQ, TK.COLN]
_ASSIGNMENT_TOKENS_REF = [TK.COEQ, TK.EQLS, TK.EQGT, TK.ASSIGN, TK.COLN]
_FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.APPLY, TK.RARR]

_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.DATASET, TCL.IDENTIFIER, TCL.TUPLE, TCL.FUNCTION]
_IDENTIFIER_TOKENS = [TK.IDNT, TK.ANON, TK.REF, TK.DOT, TK.TUPLE, TK.FUNCTION]
_IDENTIFIER_TOKENS_EX = [TK.IDNT, TK.ANON, TK.REF, TK.DOT, TK.TUPLE, TK.FUNCTION, TK.COLN, TK.BLOCK, TK.BUY, TK.SELL,
                         TK.CHAIN]
_VALUE_TOKENS = [TK.BOOL, TK.FLOT, TK.EMPTY, TK.INT, TK.NONE, TK.STR, TK.DUR, TK.OBJECT, TK.SET, TK.LIST, TK.IDNT]

_ADDITION_TOKENS = [TK.PLUS, TK.MNUS, TK.SUB, TK.ADD]
_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR, TK.FALL_BELOW, TK.RISE_ABOVE]
_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ, TK.ISEQ]
_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS, TK.CLN2, TK.QSTN]
_MULTIPLICATION_TOKENS = [TK.SLSH, TK.DIV, TK.STAR, TK.MUL, TK.EXPN, TK.POW, TK.DOT, TK.DOT2,
                          TK.RANGE, TK.IDIV, TK.MOD]
_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL, TK.MNU2, TK.PLU2]
_SET_UNARY_TOKENS = [TK.NONE, TK.ALL, TK.ANY]

_EXPRESSION_TOKENS = _ADDITION_TOKENS + _MULTIPLICATION_TOKENS + _UNARY_TOKENS \
                     + _LOGIC_TOKENS + _EQUALITY_TEST_TOKENS + _COMPARISON_TOKENS + _SET_UNARY_TOKENS
