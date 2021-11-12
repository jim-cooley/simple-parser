from enum import unique, IntEnum, auto

from environment.token_ids import TK


# character class definitions: these need to be coordinated with column order in the state table
@unique
class CL(IntEnum):
    EOF = 0  # (EOF)
    NONE = 1  #
    LETR = 2  # [A-Z][a-z]
    DIGT = 3  # [0-9]
    USCR = 4  # _
    SEMI = 5  # ;
    COMA = 6  # ,
    DOT = 7  # .
    COLN = 8  # :
    MNUS = 9  # -
    PLUS = 10  # +
    STAR = 11  # *
    SLSH = 12  # /
    BSLH = 13  # \
    PCT = 14  # %
    EXPN = 15  # ^
    EQLS = 16  # =
    LBS = 17  # #
    SQOT = 18  # '
    DQOT = 19  # "
    EXCL = 20  # !
    QSTN = 21  # ?
    AMPS = 22  # &
    DLRS = 23  # $
    ATS = 24  # @
    BAR = 25  # |
    GTR = 26  # >
    LESS = 27  # <
    LBRC = 28  # {
    RBRC = 29  # }
    LPRN = 30  # (
    RPRN = 31  # )
    LBRK = 32  # [
    RBRK = 33  # ]
    TLDE = 34  # ~
    SPEC = 35  # special characters
    NEWLN = 36  # \n
    WHITE = 37  # \t, ' '
    #
    MAX = 38


cClass = [
    #   0        1        2       3        4        5        6        7        8        9              0123456789
    CL.EOF,  CL.NONE, CL.NONE,CL.NONE,  CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.WHITE,  # 00  .......\a.\t
    CL.NEWLN,CL.NONE, CL.NONE,CL.WHITE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 10  \v.\r\f...... ## \n = \r+\v
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 20  ..........
    CL.NONE, CL.NONE, CL.WHITE,CL.EXCL, CL.DQOT, CL.LBS,  CL.DLRS, CL.PCT,  CL.AMPS, CL.SQOT,   # 30  .. !"#$%&'
    CL.LPRN, CL.RPRN, CL.STAR, CL.PLUS, CL.COMA, CL.MNUS, CL.DOT,  CL.SLSH, CL.DIGT, CL.DIGT,   # 40  ()*+,-./01
    CL.DIGT, CL.DIGT, CL.DIGT, CL.DIGT, CL.DIGT, CL.DIGT, CL.DIGT, CL.DIGT, CL.COLN, CL.SEMI,   # 50  23456789:;
    CL.LESS, CL.EQLS, CL.GTR,  CL.QSTN, CL.ATS,  CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR,   # 60  <=>?@ABCDE
    CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR,   # 70  FGHIJKLMNO
    CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR,   # 80  PQRSTUVWXY
    CL.LETR, CL.LBRK, CL.BSLH, CL.RBRK, CL.EXPN, CL.USCR, CL.SQOT, CL.LETR, CL.LETR, CL.LETR,   # 90  Z[\]^_`abc
    CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR,   # 100 defghijklm
    CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR, CL.LETR,   # 110 nopqrstuvw
    CL.LETR, CL.LETR, CL.LETR, CL.LBRC, CL.BAR,  CL.RBRC, CL.TLDE, CL.NONE, CL.NONE, CL.NONE,   # 120 xwz{|}~...
    # python bytes from ascii text can only be in range 0..127
    # supported extended ascii characters shown for reference. these are mapped in u16_to_chid()
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 130 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 140 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 150 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 160 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 170 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 180 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 190 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 200 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.SPEC, CL.NONE, CL.NONE, CL.NONE,   # 210 ......Ø...
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 220 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,   # 230 ..........
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.SPEC, CL.NONE,   # 240 ........ø.
    CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE, CL.NONE,                                       # 250 .....
    # utf-8 code page 0..255
]


# tokenizer states. these need to match the order of the state-table, so do not use 'auto'
@unique
class ST(IntEnum):
    MAIN = 0
    IDNT = 1        # Identifier lexer
    INT = auto()    # Int / Float lexer
    FLOT = auto()   # Floating point lexer
    WHT = auto()    # whitepace consumer
    SCMT = auto()   # single-line comment extractor
    SQOT = auto()   # quoted string (single)
    DQOT = auto()   # quoted string (double)
    CMCT = auto()   # c-style multi-line comment extractor (/*...*/)
    SLSH = auto()   # '/' disambiguator (c-style)
    STAR = auto()   # '*' disambiguator (in c-style comment
    PMCT = auto()   # py-style multi-line comment extractor ('''...''')
    SQT1 = auto()   # py-style single-quote disambiguator 1 (entry)
    SQT2 = auto()   # py-style single-quote disambiguator 2 (entry)
    SQT3 = auto()   # py-style single-quote disambiguator 3 (exit)
    SQT4 = auto()   # py-style single-quote disambiguator 4 (exit)
    GTR2 = auto()   # > disambiguation (>, >=, >>)
    LSS2 = auto()   # < disambiguation (<, <=, <<)
    EQLS = auto()   # = disambiguation (=, ==, =>)
    EXCL = auto()   # ! disambiguation (!, !=)
    COLN = auto()   # : disambiguation (:, ::, :=, :-)
    BAR = auto()    # | disambiguation (|, ||, |=)
    MNUS = auto()   # - disambiguation (-, -=, --)
    PLUS = auto()   # + disambiguation (+, +=, ++)
    DOT = auto()    # . disambiguation (., ..)
    PCT = auto()    # % disambiguation (%, %%)
    TIME = auto()   # parse time hh:mm:ss...
    CURR = auto()   # parse currency
    MAX = 31  # states > here are token ids


#
# tokenizer scanning state table: yep, totally violates PEP8
#
tkState = [
    #   0        1        2        3        4        5        6        7        8        9        10       1        2        3        4        5        6        7        8        9        20       1        2        3        4        5        6        7        8        9        30       1        2        3        4        5        6        7        8        9        40
    # CL.EOF,  CL.NONE, CL.LETR, CL.DIGT, CL.USCR, CL.SEMI, CL.COMA, CL.DOT,  CL.COLN, CL.MNUS, CL.PLUS, CL.STAR, CL.SLSH, CL.BSLH, CL.PCT,  CL.EXPN, CL.EQLS, CL.LBS,  CL.SQOT, CL.DQOT, CL.EXCL, CL.QSTN, CL.AMPS, CL.DLRS, CL.ATS,  CL.BAR,  CL.GTR,  CL.LESS, CL.LBRC, CL.RBRC, CL.LPRN, CL.RPRN, CL.LBRK, CL.RBRK, CL.TLDE, CL.SPEC CL.NEWLN,CL.WHITE,
# 0: ST.MAIN  - main scanning loop
    [-TK.EOF,  TK.BAD,  ST.IDNT, ST.INT,  ST.IDNT, TK.SEMI, TK.COMA, ST.DOT,  ST.COLN, ST.MNUS, ST.PLUS, TK.STAR, ST.SLSH, TK.BSLH, ST.PCT,  TK.EXPN, ST.EQLS,-ST.SCMT,-ST.SQT1,-ST.DQOT, ST.EXCL, TK.QSTN, TK.AMPS,-ST.CURR, TK.ATS,  ST.BAR,  ST.GTR2, ST.LSS2, TK.LBRC, TK.RBRC, TK.LPRN, TK.RPRN, TK.LBRK, TK.RBRK, TK.BAD, TK.SPEC, TK.EOL, ST.WHT],

# 1: ST.IDENT - extract identifiers
    [-TK.IDNT,-TK.IDNT, ST.IDNT, ST.IDNT, ST.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT,-TK.IDNT],

# 2: ST.INT   - extract integers
    [-TK.INT, -TK.INT,  TK.DUR,  ST.INT, -TK.INT, -TK.INT, -TK.INT,  ST.FLOT, ST.TIME,-TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT,  TK.PCT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT, -TK.INT,-TK.INT, -TK.INT],

# 3: ST.FLOT - extract floats (& currency)
    [-TK.FLOT, -TK.FLOT,TK.DUR,  ST.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT, TK.PCT, -TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT],

# 4: ST.WHITE - whitespace scanner
    [-TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT, -TK.WHT,  ST.WHT],

# 5: ST.SCMT- skip single-line comments (c- or python-style)
    [-TK.EOL, -ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.SCMT,-ST.WHT,  TK.EOL, -ST.SCMT],

# 6: ST.SQOT - single-quoted literal (skip past ")
    [TK.ERR,   ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT,-TK.QUOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT],

# 7: ST.DQOT - double-quoted literal (skip past ')
    [TK.ERR,   ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT,-TK.QUOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT, ST.DQOT],

# 8: ST.CMCT- skip C-style multi-line comments
    [-TK.ERR, -ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.STAR,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT],

# 9: ST.SLSH- forward slash disambiguator (c-style)
    [-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-ST.CMCT,-ST.SCMT,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH,-TK.SLSH],

# 10: ST.STAR- asterisk disambiguator (in c-style ML comment)
    [-TK.ERR, -ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-TK.WHT, -ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT,-ST.CMCT],

# 11: ST.PMCT- skip Python-style multi-line comments
    [-TK.ERR, -ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.SQT3,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT],

# 12: ST.SQT1- skip Python-style multi-line comments
    [-TK.ERR,  ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT,-ST.SQT1, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT, ST.SQOT,ST.SQOT, ST.SQOT],

# 12: ST.SQT2- skip Python-style multi-line comments
    [-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-ST.PMCT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT,-TK.QUOT],

# 14: ST.SQT3- skip Python-style multi-line comments
    [-TK.ERR, -ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.SQT4,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT],

# 15: ST.SQT4- skip Python-style multi-line comments
    [-TK.ERR, -ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-TK.WHT, -ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT,-ST.PMCT],

# 16: ST.GTR2- > disambiguation
    [-TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR,  TK.GTE, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR,  -TK.GTR, TK.GTR2, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR, -TK.GTR,-TK.GTR, -TK.GTR],

# 17: ST.LSS2- < disambiguation
    [-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS, TK.LTE, -TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS, TK.LBAR,-TK.LESS, TK.LSS2,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS,-TK.LESS],

# 18: ST.EQLS- = disambiguation
    [-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS, TK.EQEQ,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS, TK.EQGT,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS,-TK.EQLS],

# 19: ST.EXCL- ! disambiguation
    [-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL, TK.NEQ, -TK.EXCL,-TK.EXCL,-TK.EXCL, TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL,-TK.EXCL],

# 20: ST.COLN- : disambiguation
    [-TK.COLN, -TK.COLN, -TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,TK.CLN2,TK.COMN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN, TK.COEQ,-TK.COLN,-TK.COLN,-TK.COLN, TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN, -TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN,-TK.COLN],

# 11: ST.BAR-  | disambiguation
    [-TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR,  TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR,  TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR,  TK.BAR2, TK.RBAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR, -TK.BAR],

# 22: ST.MNUS- - disambiguation
    [-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS, TK.MNU2,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS, TK.MNEQ,-TK.MNUS,-TK.MNUS,-TK.MNUS, TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS, TK.RARR,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS,-TK.MNUS],

# 23: ST.PLUS- + disambiguation
    [-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS, TK.PLU2,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS, TK.PLEQ,-TK.PLUS,-TK.PLUS,-TK.PLUS, TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS, TK.RARR,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS,-TK.PLUS],

# 24: ST.DOT- . disambiguation
    [-TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT,  TK.DOT2,-TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT,-TK.DOT, -TK.DOT, -TK.DOT,  TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT,  -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT, -TK.DOT,-TK.DOT, -TK.DOT],

# 25: ST.PCT- % disambiguation
    [-TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, TK.PCT2, -TK.PCT, -TK.PCT,-TK.PCT, -TK.PCT, -TK.PCT,  TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT,  -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT, -TK.PCT,-TK.PCT, -TK.PCT],

# 25: ST.TIME - extract time values
    [-TK.TIME,-TK.TIME, TK.TIME, ST.TIME,-TK.TIME, -TK.TIME,-TK.TIME,ST.TIME,ST.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,-TK.TIME,TK.TIME,-TK.TIME],

# 26: ST.CURR - extract floats (& currency)
    [-TK.FLOT, -TK.FLOT,TK.DUR,  ST.CURR,-TK.FLOT,-TK.FLOT,-TK.FLOT, ST.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT, TK.PCT, -TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT,-TK.FLOT],
]
