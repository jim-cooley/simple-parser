from dataclasses import dataclass

from runtime.scope import Scope
from runtime.token_class import TCL
from runtime.token_ids import TK

from runtime.intrinsics import load_intrinsics, load_intrinsics_not_impl


@dataclass
class Keywords(Scope):
    def __init__(self, parent_scope=None):
        super().__init__(name='_keywords', parent_scope=parent_scope)
        self.load_keywords()
        self.load_intrinsics()
        self.load_intrinsics_not_impl()

    # Keywords are r/o
    def __setitem__(self, key, value):
        return

    # cannot add to the keywords dynamically
    def define(self, name=None, value=None, token=None, local=False, update=False):
        assert False, "Attempt to add to keyword scope."

    def load_keywords(self, keywords=None):
        keywords = keywords if keywords is not None else _KEYWORDS
        for (tkid, typ, val) in keywords:
            self._add_symbol(tkid=tkid, tcl=typ, lex=val)

    def load_intrinsics(self):
        intrinsics = load_intrinsics(parent=self)
        for fname, fn in intrinsics.items():
            self._add_name(fname, fn)

    def load_intrinsics_not_impl(self):
        not_impl = load_intrinsics_not_impl()
        for fname, fn in not_impl.items():
            self._add_name(fname, fn)

    @staticmethod
    def INDEX():
        return 'index'

    @staticmethod
    def NAME():
        return 'name'


# UNDONE: True, False, None, NaN, Empty could all be identifiers/Literals and not Keywords
_KEYWORDS = [
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.ELSE, TCL.KEYWORD, 'else'),
    (TK.EMPTY, TCL.KEYWORD, "Empty"),
    (TK.EMPTY, TCL.KEYWORD, "empty"),   # UNDONE: NumPy uses this to create an empty array of size
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.THEN, TCL.KEYWORD, 'then'),
    (TK.IDENT, TCL.KEYWORD, 'apply'),
    (TK.IDENT, TCL.KEYWORD, 'expr'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.NAN, TCL.KEYWORD, 'NaN'),
    (TK.NAN, TCL.KEYWORD, 'nan'),
    (TK.NONE, TCL.KEYWORD, 'none'),
    (TK.RETURN, TCL.KEYWORD, "return"),
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.TRUE, TCL.KEYWORD, 'true'),

    # special identities
    (TK.ANON, TCL.IDENTIFIER, '_'),
    (TK.IDENT, TCL.IDENTIFIER, 'pi'),
    (TK.IDENT, TCL.IDENTIFIER, 'index'),
    (TK.IDENT, TCL.IDENTIFIER, 'name'),

    # unary
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.DEFINE, TCL.UNARY, 'def'),
    (TK.VAL, TCL.UNARY, 'val'),         # immutable (default)
    (TK.VAR, TCL.UNARY, 'var'),         # non-immutable

    # binops
    (TK.AND, TCL.BINOP, 'and'),
    (TK.IDIV, TCL.BINOP, 'div'),
    (TK.IF, TCL.BINOP, 'if'),           # NOTE: not a keyword, this will also be the tid for the operation
    (TK.OR, TCL.BINOP, 'or'),
    (TK.MOD, TCL.BINOP, 'mod'),
    (TK.IDENT, TCL.BINOP, 'rand'),
]

