from enum import unique, IntEnum, auto

ST_MAX = 31  # ST.MAX


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
    IDENT = auto()  #
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

    # reserved identifier
    RESERVED = 200

    # last reserved token value (below 128 can be used in state machine, 128-255 error & reserved)
    #

    #
    # higher-level / derived tokens
    #
    ADD = auto()  # +
    APPLY = auto()  # >>
    ASSIGN = auto()  # =
    BLOCK = auto()
    BOOL = auto()
    CATEGORY = auto()  # category enumeration
    CHAIN = auto()
    COMMAND = auto()
    COMPARE = auto()  # ?  a ? b is to compare a to b
    DECREMENT = auto()  # --
    DEF = auto()  # set version of REF
    DEFINE = auto()  # :=, 'def'
    DEFINE_FN = auto()  # =>,  'def' f(x)
    DOTPROD = auto()  # •
    ENUM = auto()  # Integer enumeration
    EVENT = auto()  # from =>
    FALL_BELOW = auto()  # <|
    FUNCTION = auto()
    IDIV = auto()  # integer division
    INCREMENT = auto()
    ISEQ = auto()  # ==
    KVPAIR = auto()  # key:value
    LIST = auto()
    MUL = auto()  # *
    NATIVE = auto()  # token represents native literal
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
    TERNARY = auto()  # '?' operator -- <condition> ? <true> : <false>
    TUPLE = auto()

    LAST = 299  # last reserved token id

    # keywords & intrinsic functions
    ALL = auto()  # all:
    AND = auto()
    ANON = auto()  # anonymous parameter '_'
    ANY = auto()  # any:
    BUY = auto()
    DATASET = auto()
    DIV = auto()  # /
    ELSE = auto()
    EMPTY = auto()  # ø empty set
    FALSE = auto()
    IF = auto()
    IN = auto()
    INDEX = auto()
    MOD = auto()
    NAN = auto()
    NONE = auto()
    NONEOF = auto()  # none:
    NOT = auto()
    NOW = auto()
    RETURN = auto()
    RANGE = auto()
    SELL = auto()
    THEN = auto()
    TODAY = auto()
    TRUE = auto()
    VAR = auto()
