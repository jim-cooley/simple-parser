# abstract syntax trees:
from dataclasses import dataclass

from tokens import TCL, TK, Token


@dataclass
class AST(object):
    parent = None

    def __getattr__(self, item):
        if item == 'properties':
            return self.token.properties
        elif item == 'value':
            return self.token.value

    def __setattr__(self, name, value):
        if name == 'value':
            self.token.value = value
        else:
            super().__setattr__(name, value)

    def __str__(self):
        if getattr(self, 'format', None) is not None:
            return self.format()
        return self.__repr__()


# base classes:
@dataclass
class BinOp(AST):
    def __init__(self, left, op, right):
        op.t_class = TCL.BINOP
        self.left = left
        self.right = right
        self.token = op
        self.op = op.id
        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'BinOp({self.token}: l={left}, r={right}'


@dataclass
class Literal(AST):
    def __init__(self, token):
        token.t_class = TCL.LITERAL
        self.token = token
        if token is not None:
            self.token.id = token.map2litval().id
            self.value = token.value


@dataclass
class UnaryOp(AST):
    def __init__(self, token, expr):
        token.t_class = TCL.UNARY
        self.token = token
        self.op = token.id
        self.expr = expr
        if expr is not None:
            expr.parent = self


# derived classes
@dataclass
class Command(UnaryOp):
    def __init__(self, token, expr):
        super().__init__(token, expr)


@dataclass
class FnCall(BinOp):
    def __init__(self, token, plist, op=None):
        op = Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex="(", loc=token.location) if op is None else op
        super().__init__(left=Ident(token), op=op, right=plist)


@dataclass
class Ident(Literal):
    def __init__(self, token):
        tcl = token.t_class
        super().__init__(token)
        token.t_class = tcl
        self.value = token.lexeme


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
    def __init__(self, token, prop, op=None):
        op = Token(tid=TK.REF, tcl=TCL.BINOP, lex=".", loc=token.location) if op is None else op
        super().__init__(left=Ident(token), op=op, right=prop)
