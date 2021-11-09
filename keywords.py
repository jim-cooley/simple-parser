from dataclasses import dataclass

from scope import Scope
from tokens import TK, TCL


@dataclass
class Keywords(Scope):
    def __init__(self, parent_scope=None):
        super().__init__(parent_scope)
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
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.AND, TCL.BINOP, 'and'),
    (TK.ANON, TCL.IDENTIFIER, '_'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.BUY, TCL.KEYWORD, "buy"),
    (TK.DEFINE, TCL.UNARY, 'def'),
    (TK.EMPTY, TCL.KEYWORD, "Empty"),
    (TK.EMPTY, TCL.KEYWORD, "empty"),
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.IDIV, TCL.BINOP, 'div'),
    (TK.IDNT, TCL.BINOP, 'index'),
    (TK.IDNT, TCL.BINOP, 'rand'),
    (TK.IDNT, TCL.DATASET, "close"),
    (TK.IDNT, TCL.DATASET, "high"),
    (TK.IDNT, TCL.DATASET, "low"),
    (TK.IDNT, TCL.DATASET, "open"),

    (TK.DATASET, TCL.FUNCTION, 'Dataset'),
    (TK.DATASET, TCL.FUNCTION, 'dataset'),
    (TK.IDNT, TCL.FUNCTION, "ema"),
    (TK.IDNT, TCL.FUNCTION, "sma"),
    (TK.IDNT, TCL.FUNCTION, 'columns'),
    (TK.IDNT, TCL.FUNCTION, 'fillempty'),
    (TK.IDNT, TCL.FUNCTION, 'min'),
    (TK.IDNT, TCL.FUNCTION, 'max'),
    (TK.IDNT, TCL.FUNCTION, 'select'),
    (TK.IDNT, TCL.FUNCTION, "Series"),
    (TK.IDNT, TCL.FUNCTION, "series"),
    (TK.IDNT, TCL.FUNCTION, "signal"),
    (TK.IDNT, TCL.FUNCTION, 'today'),

    (TK.IDNT, TCL.KEYWORD, 'apply'),
    (TK.IDNT, TCL.KEYWORD, 'expr'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.IDNT, TCL.FUNCTION, 'index'),
    (TK.MOD, TCL.BINOP, 'mod'),
    (TK.NAN, TCL.KEYWORD, 'NaN'),
    (TK.NAN, TCL.KEYWORD, 'nan'),
    (TK.NONE, TCL.KEYWORD, 'none'),
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.NOW, TCL.KEYWORD, 'now'),
    (TK.OR, TCL.BINOP, 'or'),
    (TK.SELL, TCL.KEYWORD, "sell"),
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.TRUE, TCL.KEYWORD, 'true'),
    (TK.VAR, TCL.UNARY, 'var'),
]

