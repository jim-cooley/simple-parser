# abstract syntax trees:
from dataclasses import dataclass

from tokens import TCL


@dataclass
class AST(object):
    def __getattr__(self, item):
        if item == 'properties':
            return self.token.properties
        elif item == 'value':
            return self.token.value
        pass


@dataclass
class BinOp(AST):
    def __init__(self, left, op, right):
        op.t_class = TCL.BINOP
        self.left = left
        self.right = right
        self.token = op
        self.op = op.id


@dataclass
class Command(AST):
    def __init__(self, token, expr):
        token.t_class = TCL.COMMAND
        self.token = token
        self.op = token.id
        self.expr = expr


@dataclass
class FnCall(AST):
    def __init__(self, token, plist):
        self.token = token
        self.parameter_list = plist


@dataclass
class Ident(AST):
    def __init__(self, token):
        self.token = token


@dataclass
class Literal(AST):
    def __init__(self, token):
        token.t_class = TCL.LITERAL
        self.token = token


@dataclass
class PropCall(AST):
    def __init__(self, token, member, plist):
        self.token = token
        self.member = member
        self.parameter_list = Seq(None, plist)


@dataclass
class PropRef(AST):
    def __init__(self, token, prop):
        self.token = token
        self.member = prop


@dataclass
class Seq(AST):
    def __init__(self, token, slist):
        self.token = token
        self.sequence = slist

    def append(self, o):
        self.sequence.append(o)


@dataclass
class UnaryOp(AST):
    def __init__(self, token, expr):
        token.t_class = TCL.UNARY
        self.token = token
        self.op = token.id
        self.expr = expr


class NodeVisitor(object):
    def visit(self, node):
        if node is not None:
            method_name = 'visit_' + type(node).__name__
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
