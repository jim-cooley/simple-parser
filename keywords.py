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
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.BUY, TCL.KEYWORD, "buy"),   # UNDONE: remove 'buy' as keyword.
    (TK.EMPTY, TCL.KEYWORD, "Empty"),
    (TK.EMPTY, TCL.KEYWORD, "empty"),   # UNDONE: NumPy uses this to create an empty array of size
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.IDNT, TCL.KEYWORD, 'apply'),
    (TK.IDNT, TCL.KEYWORD, 'expr'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.IDNT, TCL.FUNCTION, 'index'),
    (TK.NAN, TCL.KEYWORD, 'NaN'),
    (TK.NAN, TCL.KEYWORD, 'nan'),
    (TK.NONE, TCL.KEYWORD, 'none'),
    (TK.NOW, TCL.KEYWORD, 'now'),
    (TK.SELL, TCL.KEYWORD, "sell"), # UNODNE: remove sell as a keyword
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.TRUE, TCL.KEYWORD, 'true'),

    # special identities
    (TK.ANON, TCL.IDENTIFIER, '_'),
    (TK.IDNT, TCL.IDENTIFIER, 'pi'),
    (TK.IDNT, TCL.IDENTIFIER, 'today'),

    # type constructors
    (TK.DATASET, TCL.FUNCTION, 'Dataset'),
    (TK.DATASET, TCL.FUNCTION, 'dataset'),
    (TK.IDNT, TCL.FUNCTION, "Series"),
    (TK.IDNT, TCL.FUNCTION, "series"),

    # unary
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.DEFINE, TCL.UNARY, 'def'),
    (TK.VAR, TCL.UNARY, 'var'),

    # binops
    (TK.AND, TCL.BINOP, 'and'),
    (TK.IDIV, TCL.BINOP, 'div'),
    (TK.IDNT, TCL.BINOP, 'index'),
    (TK.OR, TCL.BINOP, 'or'),
    (TK.MOD, TCL.BINOP, 'mod'),
    (TK.IDNT, TCL.BINOP, 'rand'),

    # functions (intrinsics)
    (TK.IDNT, TCL.FUNCTION, "ema"),
    (TK.IDNT, TCL.FUNCTION, "sma"),
    (TK.IDNT, TCL.FUNCTION, 'columns'),
    (TK.IDNT, TCL.FUNCTION, 'fillempty'),
    (TK.IDNT, TCL.FUNCTION, 'select'),
    (TK.IDNT, TCL.FUNCTION, "signal"),

    # NumPy
    (TK.IDNT, TCL.FUNCTION, 'arrange'),     # create array of evenly spaced values
    (TK.IDNT, TCL.FUNCTION, 'corrcoef'),    # correlation coefficient
    (TK.IDNT, TCL.FUNCTION, 'cos'),
    (TK.IDNT, TCL.FUNCTION, 'cumsum'),      # cummulative sum
    (TK.IDNT, TCL.FUNCTION, 'dot'),         # CONSIDER: turn this into operator ?
    (TK.IDNT, TCL.FUNCTION, 'eye'),         # create identity matrix
    (TK.IDNT, TCL.FUNCTION, 'exp'),
    (TK.IDNT, TCL.FUNCTION, 'fill'),        # create a constant array (np: full)
    (TK.IDNT, TCL.FUNCTION, 'log'),
    (TK.IDNT, TCL.FUNCTION, 'linspace'),    # create array of evenly spaced values (number of samples)
    (TK.IDNT, TCL.FUNCTION, 'max'),
    (TK.IDNT, TCL.FUNCTION, 'mean'),
    (TK.IDNT, TCL.FUNCTION, 'median'),
    (TK.IDNT, TCL.FUNCTION, 'min'),
    (TK.IDNT, TCL.FUNCTION, 'ones'),        # create an array of ones
    (TK.IDNT, TCL.FUNCTION, 'random'),      # create array of random values
    (TK.IDNT, TCL.FUNCTION, 'rand'),        # generate a random number (single sample)
    (TK.IDNT, TCL.FUNCTION, 'std'),         # standard deviation
    (TK.IDNT, TCL.FUNCTION, 'sqrt'),
    (TK.IDNT, TCL.FUNCTION, 'sin'),
    (TK.IDNT, TCL.FUNCTION, 'sum'),
    (TK.IDNT, TCL.FUNCTION, 'zeros'),       # create an array of zeros

    # Pandas
    (TK.IDNT, TCL.FUNCTION, 'rank'),        # assign ranks to entries

    # I/O
    (TK.IDNT, TCL.FUNCTION, 'load'),        # format=numpy will load numpy data, format=txt will save text. fomats to support: focal, numpy, pandas, excel, csv, text/other
    (TK.IDNT, TCL.FUNCTION, 'save'),        # format=numpy will save numpy data, format=txt will save text

]

