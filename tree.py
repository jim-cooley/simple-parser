# abstract syntax trees:
from dataclasses import dataclass
from tokens import TCL


# base classes:
@dataclass
class AST:
    def __init__(self, token=None, value=None, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.token = token
        if token is not None and value is not None:
            token.value = value

    def __get__(self):
        return self.value

    @property
    def value(self):
        return self.token.value if self.token is not None else None

    @value.setter
    def value(self, value):
        self.token.value = value

    def __str__(self):
        if getattr(self, 'format', None) is not None:
            return self.format()
        return self.__repr__()


@dataclass
class BinOp(AST):
    def __init__(self, left, op, right):
        super().__init__(token=op)
        op.t_class = TCL.BINOP
        self.left = left
        self.right = right
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
class UnaryOp(AST):
    def __init__(self, token, expr):
        super().__init__(token=token)
        token.t_class = TCL.UNARY
        self.op = token.id
        self.expr = expr
        if expr is not None:
            expr.parent = self


@dataclass
class Command(UnaryOp):
    def __init__(self, token, expr):
        super().__init__(token, expr)
