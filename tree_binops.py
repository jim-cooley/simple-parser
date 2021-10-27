from dataclasses import dataclass

from scope import Ident
from tokens import Token, TK, TCL
from tree import BinOp


@dataclass
class FnCall(BinOp):
    def __init__(self, token, plist, op=None):
        op = Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex="(", loc=token.location) if op is None else op
        super().__init__(left=Ident(token), op=op, right=plist)


@dataclass
class Index(FnCall):
    def __init__(self, token, plist):
        super().__init__(token, plist, op=Token(tid=TK.INDEX, tcl=TCL.BINOP, lex="[", loc=token.location))


@dataclass
class PropCall(FnCall):
    def __init__(self, token, member, plist):
        super().__init__(token, plist, op=Token(tid=TK.REF, tcl=TCL.FUNCTION, lex=".(", loc=token.location))


@dataclass
class PropRef(BinOp):
    def __init__(self, token, prop, op=None, ref=False):
        op = Token(tid=TK.REF if ref is True else TK.DEF, tcl=TCL.BINOP, lex=".",
                   loc=token.location) if op is None else op
        super().__init__(left=Ident(token), op=op, right=prop)
