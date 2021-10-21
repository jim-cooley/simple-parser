# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy
from dataclasses import dataclass

from tokens import TCL, TK, Token
from tree import AST

_KEYWORDS = [
    (TK.BUY, TCL.KEYWORD, "buy"),
    (TK.SELL, TCL.KEYWORD, "sell"),
    (TK.SIGNAL, TCL.KEYWORD, "signal"),
    (TK.IDNT, TCL.DATASET, "open"),
    (TK.IDNT, TCL.DATASET, "close"),
    (TK.IDNT, TCL.DATASET, "high"),
    (TK.IDNT, TCL.DATASET, "low"),
    (TK.IDNT, TCL.FUNCTION, "sma"),
    (TK.IDNT, TCL.FUNCTION, "ema"),
    (TK.AND, TCL.LOGICAL, 'and'),
    (TK.OR, TCL.LOGICAL, 'or'),
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.NONEOF, TCL.KEYWORD, 'none'),
    (TK.TRUE, TCL.KEYWORD, 'true'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.NONE, TCL.KEYWORD, 'None'),
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.DEFINE, TCL.UNARY, 'def'),

    (TK.FUNCTION, TCL.KEYWORD, 'apply'),
    (TK.FUNCTION, TCL.KEYWORD, 'columns'),
    (TK.FUNCTION, TCL.KEYWORD, 'expr'),
    (TK.FUNCTION, TCL.KEYWORD, 'fillempty'),
    (TK.FUNCTION, TCL.KEYWORD, 'select')
]


@dataclass
class Scope(AST):
    parent = None
    _symbols = {}

    def __init__(self, parent=None):
        self.parent = parent

    def __getitem__(self, key):
        return self.find(key)

    def __setitem__(self, key, value):
        self.define(key, value)

    def __contains__(self, key):
        return self.contains(key)

    def assign(self, token, expr):
        self._find_add(token, expr)

    def define(self, token, expr):
        self._find_add(token, expr)

    def contains(self, token):
        return token.lexeme in self._symbols

    def find(self, token, default=None):
        if token.lexeme in self._symbols:
            return self._symbols[token.lexeme]
        return default

    def _find_add(self, token, value):
        symbol = self.find(token)
        if symbol is None:
            symbol = copy(token)
            self._symbols[token.lexeme] = value
        return symbol

    def _add_symbol(self, tkid, tcl, lex):
        tk = Token(tid=tkid, tcl=tcl, lex=lex, loc=Token.Loc())
        self._symbols[lex] = tk

    def print(self, indent=0):
        spaces = '' if indent < 1 else ' '.ljust(indent * 4)
        for k in self._symbols.keys():
            print(f'{spaces}{k}: {self._symbols[k]}')


@dataclass
class Keywords(Scope):
    def __init__(self):
        super().__init__()
        self.load_keywords()

    # Keywords are r/o
    def __setitem__(self, key, value):
        return

    def define(self, token, expr):
        return

    def load_keywords(self, keywords=_KEYWORDS):
        for (tkid, typ, val) in keywords:
            self._add_symbol(tkid, typ, val)
