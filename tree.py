# abstract syntax trees:
from dataclasses import dataclass

from symbols import SymbolTable
from tokens import TCL, TK, Token


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

    def __getitem__(self, item):
        return self.values()[item]

    def values(self):
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
class Set(Seq):
    def __init__(self, token, dict=None):
        super().__init__(token, dict)
        token.id = TK.SET
        token.t_class = TCL.SET
        token.value = None if dict is None else dict
        self.value = dict

    def __getitem__(self, item):
        if type(item).name == 'int':
            return self.values()[item]
        return self.value[item]

    def keys(self):
        return list(self.value.keys())

    def values(self):
        return self.value if type(self.value).__name__ == "list" else list(self.value.values())

    def tuples(self):
        return list(self.value.items())

    def format(self):
        if self.value is None:
            return '{}'
        else:
            return '{' + self.value + '}'


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


@dataclass
class Index(FnCall):
    def __init__(self, token, plist):
        super().__init__(token, plist, Token(tid=TK.INDEX, tcl=TCL.BINOP, lex="[", loc=token.location))


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
