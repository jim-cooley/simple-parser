# abstract syntax trees:
from dataclasses import dataclass

from tokens import TCL, Token, TK


# base classes:
@dataclass
class AST:
    def __init__(self, token=None, value=None, parent=None, **kwargs):
        super().__init__(**kwargs)
        self .parent = parent
        self.token = token
        if token is not None and value is not None:
            token.value = value

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


# a compound node containing a sequence of 'items'
@dataclass
class ASTCompound(AST):
    def __init__(self, token=None, value=None, parent=None, **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.items = []

    @property
    def last(self):
        return self.items[len(self.items) - 1]

    @last.setter
    def last(self, value):
        self.items[len(self.items) - 1] = value

    def append(self, item):
        self.items.append(item)

    def len(self):
        return len(self.items)

    def values(self):
        return self.items

    def format(self):
        if self.value is None:
            return '{}'
        else:
            fstr = ''
            max = (len(self.value)-1)
            for idx in range(0, len(self.value)):
                fstr += f'{self.items[idx]}'
                fstr += ',' if idx < max else ''
            return '{' + f'{fstr}' + '}'


@dataclass
class Expression(ASTCompound):
    def __init__(self, token=None, value=None, parent=None, is_lvalue=True, **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


@dataclass
class Statement(ASTCompound):
    def __init__(self, token=None, value=None, parent=None, is_lvalue=True,  **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


# -----------------------------------
# Expression Nodes
# -----------------------------------
@dataclass
class Assign(Expression):
    def __init__(self, left, op, right, is_lvalue=None):
        super().__init__(token=op, is_lvalue=False if is_lvalue is None else is_lvalue)
#       self.token = left.token
        self.left = left
        self.right = right
        self.op = TK.ASSIGN
        if right is not None:
            right.parent = self

    def format(self):
        left = "None" if self.token is None else f'{self.token}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'Assign({self.op}, {self.token}: l={left}, r={right})'


@dataclass
class BinOp(Expression):
    def __init__(self, left, op, right, is_lvalue=None):
        super().__init__(token=op, is_lvalue=True if is_lvalue is None else is_lvalue)
        op.t_class = TCL.BINOP
        self.left = left
        self.right = right
        self.op = op.id
        if left is not None:
            left.parent = self
            self.is_lvalue &= left.is_lvalue
        if right is not None:
            right.parent = self
            self.is_lvalue &= right.is_lvalue

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'BinOp({self.token}: l={left}, r={right}'


# allowed to set values
@dataclass
class Define(Assign):
    def __init__(self, left, op, right, is_lvalue=None):
        is_lvalue = False if op.id != TK.COLN else is_lvalue
        super().__init__(left=left, op=op, right=right, is_lvalue=True if is_lvalue is None else is_lvalue)
        self.op = TK.DEFINE
        if right is not None:
            self.is_lvalue = right.is_lvalue

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'Define({self.op}, {self.token}: l={left}, r={right})'


@dataclass
class ApplyChainProd(Define):
    def __init__(self, left, op):
        super().__init__(left=left, op=op, right=None, is_lvalue=False)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'ApplyChainProd({self.op}, {self.token}: l={left}, r={right})'


# evaluated each access
@dataclass
class DefineFn(Define):
    def __init__(self, left, op, right):
        super().__init__(left=left, op=op, right=right, is_lvalue=False)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'DefineFn({self.op}, {self.token}: l={left}, r={right})'


# value takes on defined range during iteration
@dataclass
class DefineVar(Define):
    def __init__(self, left, op, right, is_lvalue=None):
        super().__init__(left=left, op=op, right=right, is_lvalue=False if is_lvalue is None else is_lvalue)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'DefineVar({self.op}, {self.token}: l={left}, r={right})'


# value takes on defined range during iteration, and is evaluated each time
@dataclass
class DefineVarFn(DefineVar):
    def __init__(self, left, op, right):
        super().__init__(left=left, op=op, right=right, is_lvalue=False)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'DefineVarFn({self.op}, {self.token}: l={left}, r={right})'


@dataclass
class FnCall(BinOp):
    def __init__(self, token, plist, op=None):
        op = Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex="(", loc=token.location) if op is None else op
        super().__init__(left=Get(token), op=op, right=plist, is_lvalue=False)


# holds a reference
class Ref(Expression):
    def __init__(self, r_token):
        super().__init__(token=r_token)
        self.token = r_token
        r_token.t_class = TCL.IDENTIFIER

    def to_get(self):
        get = Get(self.token)
        get.parent = self.parent
        return get

    def format(self):
        token = 'None' if self.token is None else f'{self.token}'
        return f'Ref({token})'


# dereferences to value
class Get(Ref):
    def __init__(self, r_token):
        super().__init__(r_token=r_token)
        self.token = r_token
        r_token.t_class = TCL.IDENTIFIER

    def to_ref(self):
        ref = Ref(self.token)
        ref.parent = self.parent
        return ref

    def get(self):
        return self.value

    def format(self):
        token = 'None' if self.token is None else f'{self.token}'
        return f'Get({token})'


@dataclass
class Index(FnCall):
    def __init__(self, token, plist):
        super().__init__(token, plist, op=Token(tid=TK.INDEX, tcl=TCL.BINOP, lex="[", loc=token.location))


@dataclass
class PropCall(FnCall):
    def __init__(self, token, member, plist):
        super().__init__(token, plist,
                         op=Token(tid=TK.REF, tcl=TCL.FUNCTION, lex=".(", loc=token.location))


@dataclass
class PropRef(BinOp):
    def __init__(self, token, member, op=None):
        op = Token(tid=TK.REF, tcl=TCL.BINOP, lex=".",
                   loc=token.location) if op is None else op
        super().__init__(left=Get(token), op=op, right=member)


@dataclass
class UnaryOp(Expression):
    def __init__(self, token, expr, is_lvalue=True):
        super().__init__(token=token, is_lvalue=is_lvalue)
        token.t_class = TCL.UNARY
        self.op = token.id
        self.expr = expr
        if expr is not None:
            expr.parent = self


# -----------------------------------
# Statement Nodes
# -----------------------------------
@dataclass
class Command(Statement):
    def __init__(self, token, expr):
        super().__init__(token=token)
        token.t_class = TCL.UNARY
        self.op = token.id
        self.expr = expr
        if expr is not None:
            expr.parent = self
