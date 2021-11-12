from dataclasses import dataclass

from runtime.scope import Scope, IntrinsicFunction
from runtime.token_class import TCL
from runtime.token_ids import TK

from runtime.dispatch import init_intrinsic, _intrinsic_fundesc, _intrinsic_not_impl


@dataclass
class Keywords(Scope):
    def __init__(self, parent_scope=None):
        super().__init__(parent_scope)
        self.load_keywords()
        self.load_intrinsics()
        self.load_intrinsics_not_impl()

    # Keywords are r/o
    def __setitem__(self, key, value):
        return

    # cannot add to the keywords dynamically
    def define(self, name=None, value=None, token=None, local=False, update=False):
        assert False, "Attempt to add to keyword scope."
        return None

    def load_keywords(self, keywords=None):
        keywords = keywords if keywords is not None else _KEYWORDS
        for (tkid, typ, val) in keywords:
            self._add_symbol(tkid, typ, val)

    def load_intrinsics(self, intrinsics=None):
        intrinsics = intrinsics or _intrinsic_fundesc
        for fname, desc in intrinsics.items():
            fn = init_intrinsic(fname)
            self._add_name(fname, fn)

    def load_intrinsics_not_impl(self, not_impl=None):
        not_impl = not_impl or _intrinsic_not_impl
        for fname in not_impl:
            fn = IntrinsicFunction(name=fname, tid=TK.IDNT)
            self._add_name(fname, fn)


# UNDONE: True, False, None, NaN, Empty could all be identifiers/Literals and not Keywords
_KEYWORDS = [
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.BUY, TCL.KEYWORD, "buy"),   # UNDONE: remove 'buy' as keyword.
    (TK.ELSE, TCL.KEYWORD, 'else'),
    (TK.EMPTY, TCL.KEYWORD, "Empty"),
    (TK.EMPTY, TCL.KEYWORD, "empty"),   # UNDONE: NumPy uses this to create an empty array of size
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.THEN, TCL.KEYWORD, 'then'),
    (TK.IDNT, TCL.KEYWORD, 'apply'),
    (TK.IDNT, TCL.KEYWORD, 'expr'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.IDNT, TCL.FUNCTION, 'index'),
    (TK.NAN, TCL.KEYWORD, 'NaN'),
    (TK.NAN, TCL.KEYWORD, 'nan'),
    (TK.NONE, TCL.KEYWORD, 'none'),
    (TK.RETURN, TCL.KEYWORD, "return"),
    (TK.SELL, TCL.KEYWORD, "sell"),  # UNODNE: remove sell as a keyword
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.TRUE, TCL.KEYWORD, 'true'),

    # special identities
    (TK.ANON, TCL.IDENTIFIER, '_'),
    (TK.IDNT, TCL.IDENTIFIER, 'pi'),

    # unary
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.DEFINE, TCL.UNARY, 'def'),
    (TK.VAR, TCL.UNARY, 'var'),

    # binops
    (TK.AND, TCL.BINOP, 'and'),
    (TK.IDIV, TCL.BINOP, 'div'),
    (TK.IDNT, TCL.BINOP, 'index'),  # UNDONE: 'index' appears twice.  only one survives...
    (TK.IF, TCL.BINOP, 'if'),       # NOTE: not a keyword, this will also be the tid for the operation
    (TK.OR, TCL.BINOP, 'or'),
    (TK.MOD, TCL.BINOP, 'mod'),
    (TK.IDNT, TCL.BINOP, 'rand'),
]

