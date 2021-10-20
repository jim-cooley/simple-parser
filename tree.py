# abstract syntax trees:
from dataclasses import dataclass

from symbols import SymbolTable
from tokens import TCL, TK


@dataclass
class AST(object):
    parent = None

    def __getattr__(self, item):
        if item == 'properties':
            return self.token.properties
        elif item == 'value':
            return self.token.value
        pass

    def __str__(self):
        if self.__getattr__('format') is not None:
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


@dataclass
class Literal(AST):
    def __init__(self, token):
        token.t_class = TCL.LITERAL
        self.token = token


@dataclass
class PropRef(AST):
    def __init__(self, token, prop):
        self.token = token
        self.member = prop
        if prop is not None:
            prop.parent = self


@dataclass
class Seq(AST):
    def __init__(self, token, slist):
        self.token = token
        self.value = slist

    def sequence(self):
        return self.value

    def append(self, o):
        self.value.append(o)


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
        token.t_class = TCL.COMMAND


@dataclass
class Dict(Seq):
    def __init__(self, token, dict=None):
        super().__init__(token, dict)
        token.id = TK.SET
        token.t_class = TCL.SET
        token.value = None if dict is None else dict
        self.value = dict

    def sequence(self):
        return self.value.values()

    def format(self):
        if self.value is None:
            return '{}'
        else:
            return '{' + self.value + '}'


@dataclass
class FnCall(AST):
    def __init__(self, token, plist):
        self.token = token
        self.parameter_list = plist
        if plist is not None:
            plist.parent = self


@dataclass
class Ident(Literal):
    def __init__(self, token):
        tcl = token.t_class
        super().__init__(token)
        token.t_class = tcl


@dataclass
class Index(AST):
    def __init__(self, token, plist):
        self.token = token
        self.parameter_list = plist
        if plist is not None:
            plist.parent = self


@dataclass
class PropCall(AST):
    def __init__(self, token, member, plist):
        self.token = token
        self.member = member
        self.parameter_list = Seq(None, plist)
        self.parameter_list.parent = self


@dataclass
class ParseTree(object):
    def __init__(self, nodes=None, symbols=None, source=None):
        self.nodes = nodes if nodes is not None else []
        self.symbols = symbols if symbols is not None else SymbolTable()
        self.source = source
