from dataclasses import dataclass

from scope import Scope
from tokens import TK, TCL


@dataclass
class Keywords(Scope):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_keywords()

    # Keywords are r/o
    def __setitem__(self, key, value):
        return

    def define(self, token, expr):
        return

    def load_keywords(self, keywords=None):
        keywords = keywords if keywords is not None else _KEYWORDS
        for (tkid, typ, val) in keywords:
            self._add_symbol(tkid, typ, val)


_KEYWORDS = [
    # keywords
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.BUY, TCL.KEYWORD, "buy"),
    (TK.EMPTY, TCL.KEYWORD, "empty"),
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.NONE, TCL.KEYWORD, 'none'),
#   (TK.NONEOF, TCL.KEYWORD, 'none'),
    (TK.NOW, TCL.KEYWORD, 'now'),
    (TK.SELL, TCL.KEYWORD, "sell"),
    (TK.SIGNAL, TCL.KEYWORD, "signal"),
    (TK.TODAY, TCL.KEYWORD, 'today'),
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.TRUE, TCL.KEYWORD, 'true'),

    # operators
    (TK.AND, TCL.LOGICAL, 'and'),
    (TK.DEFATTR, TCL.UNARY, 'def'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.IDIV, TCL.BINOP, 'div'),
    (TK.MOD, TCL.BINOP, 'mod'),
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.OR, TCL.LOGICAL, 'or'),
    (TK.VAR, TCL.UNARY, 'var'),

    # datasets
    (TK.IDNT, TCL.DATASET, "close"),
    (TK.IDNT, TCL.DATASET, "high"),
    (TK.IDNT, TCL.DATASET, "low"),
    (TK.IDNT, TCL.DATASET, "open"),

    # functions
    (TK.IDNT, TCL.KEYWORD, 'apply'),
    (TK.IDNT, TCL.KEYWORD, 'columns'),
    (TK.IDNT, TCL.KEYWORD, 'expr'),
    (TK.IDNT, TCL.KEYWORD, 'fillempty'),
    (TK.IDNT, TCL.KEYWORD, 'select'),
    (TK.IDNT, TCL.FUNCTION, "ema"),
    (TK.IDNT, TCL.FUNCTION, "sma"),
]
