# abstract syntax trees:
from dataclasses import dataclass

from runtime.token_data import EXPRESSION_TOKENS
from runtime.token_class import TCL
from runtime.token import Token
from runtime.token_ids import TK


# base classes:
@dataclass
class AST:
    """
    The base class of the Abstract Syntax Tree hierarchy.

    It contains a parent reference, a token, and a value.  It is built as a Mixin
    and will pass additional args and kwargs to other superclass __init__ functions.
    """

    def __init__(self, value=None, token=None, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.token = token
        self._value = value
        if value is None and token is not None:
            self._value = token.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        if getattr(self, 'format', None) is not None:
            return self.format()
        return self.__repr__()


# a compound node containing a sequence of 'items'
@dataclass
class ASTCompound(AST):
    def __init__(self, token=None, value=None, parent=None, **kwargs):
        super().__init__(value=value, token=token, parent=parent, **kwargs)
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
            max = (len(self.items) - 1)
            if max > 0:
                for idx in range(0, len(self.value)):
                    fstr += f'{self.items[idx]}'
                    fstr += ',' if idx < max else ''
            else:
                fstr = f'{self._value}'
            return '{' + f'{fstr}' + '}'


@dataclass
class Expression(ASTCompound):
    def __init__(self, value=None, token=None, parent=None, is_lvalue=True, **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


@dataclass
class Statement(ASTCompound):
    def __init__(self, value=None, token=None, parent=None, is_lvalue=True, **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


# -----------------------------------
# Base Nodes
# -----------------------------------
@dataclass
class Assign(Expression):
    def __init__(self, left, op, right, is_lvalue=None):
        super().__init__(token=op, is_lvalue=False if is_lvalue is None else is_lvalue)
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
    def __init__(self, left=None, op=None, right=None, is_lvalue=None):
        super().__init__(token=op, is_lvalue=True if is_lvalue is None else is_lvalue)
#       op.t_class = TCL.BINOP
        self.left = left
        self.right = right
        self.op = op.id
        if op.id in EXPRESSION_TOKENS:
            self.is_lvalue = False
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


@dataclass
class Define(Assign):
    """
    Base of the Definition Nodes.  In its simplest form, it Defines a symbol (variable).
    The symbol need not be defined when called.
    """

    def __init__(self, left, op, right, is_lvalue=None):
        """
        :param left: name or name Ref
        :type left: Ref
        :param op: Defining operation (=, :=, =>, ..)
        :type op: Token
        :param right: Function Block
        :type right: Block
        :param is_lvalue: Indicates whether or not this node can appear as the left-hand
        side of an assignment expression.  The default value is 'None', or unknown.
        """
        is_lvalue = False if op.id != TK.COLN else is_lvalue
        super().__init__(left=left, op=op, right=right, is_lvalue=True if is_lvalue is None else is_lvalue)
        self.op = TK.DEFINE
        if right is not None:
            self.is_lvalue = right.is_lvalue

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'Define({self.op}, {self.token}: l={left}, r={right})'


# holds a reference
class Ref(Expression):
    def __init__(self, r_token, name=None, is_lvalue=True):
        super().__init__(token=r_token, is_lvalue=is_lvalue)
        self.token = r_token
        self.name = name or r_token.lexeme
        self.location = r_token.location
        r_token.t_class = TCL.IDENTIFIER
        if r_token.is_reserved:
            self.is_lvalue = False

    def to_get(self):
        get = Get(self.token)
        get.parent = self.parent
        return get

    def format(self):
        token = 'None' if self.token is None else f'{self.token}'
        return f'Ref({token})'


@dataclass
class TernaryOp(BinOp):
    def __init__(self, op=None, left=None, mid=None, right=None, is_lvalue=True):
        assert op is not None, "Invalid operation passed to TernaryOp constructor"
        super().__init__(left=left, op=op, right=right, is_lvalue=is_lvalue)
        self.middle = mid


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
# Subclasses
# -----------------------------------
# allowed to set values
@dataclass
class Apply(Define):
    """
    Apply is a flow assignment operator.  It can be used as part of a flow to assign the
    result to a terminal expression.  It is similar to the inverse of Assign, as a >> b is
    equivalent to b = a, except: b does not need to exist beforehand, b can be a function,
    and operation proceeds left to right, not right to left.
    """
    def __init__(self, left, op=None, right=None, loc=None, is_lvalue=False):
        op = Token(tid=TK.APPLY, tcl=TCL.BINOP, lex=">>", loc=loc) if op is None else op
        super().__init__(left=left, op=op, right=right, is_lvalue=is_lvalue)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'Apply({self.op}, {self.token}: l={left}, r={right})'


@dataclass
class ApplyChainProd(Apply):
    def __init__(self, left, op, is_lvalue=False):
        op = Token(tid=TK.APPLY, tcl=TCL.BINOP, lex=">>", loc=loc) if op is None else op
        super().__init__(left=left, op=op, is_lvalue=is_lvalue)

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        return f'ApplyChainProd({self.op}, {self.token}: l={left}, r={right})'


# evaluated each access
@dataclass
class DefineFn(Define):  # left = FnRef, op=TK, plist, right = Block
    def __init__(self, left, op, right, args):
        """
        Creates a Function Definition tree node.
        :param left: FnRef for the function (name)
        :type left: Ref
        :param op: Defining operation (=, :=, =>, ..)
        :type op: Token
        :param args: Parameter list for the function
        :type args:  Tuple
        :param right: Body, Function Block
        :type right: Block
        """
        super().__init__(left=left, op=op, right=right, is_lvalue=False)
        self.args = args

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        args = 'None' if self.args is None else f'{self.args}'
        return f'DefineFn({self.op}, {self.token}: l={left}, a={args}, r={right})'


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
    def __init__(self, left, op, right, args=None):
        super().__init__(left=left, op=op, right=right, is_lvalue=False)
        self.args = args

    def format(self):
        left = "None" if self.left is None else f'{self.left}'
        right = 'None' if self.right is None else f'{self.right}'
        args = 'None' if self.args is None else f'{self.args}'
        return f'DefineVarFn({self.op}, {self.token}: l={left}, a={args}, r={right})'


# dereferences to value
class Get(Ref):
    def __init__(self, r_token, name=None, is_lvalue=True):
        super().__init__(r_token=r_token, name=name, is_lvalue=is_lvalue)

    def to_ref(self):
        ref = Ref(self.token)
        ref.parent = self.parent
        return ref

    def get(self):
        return self._value

    def format(self):
        token = 'None' if self.token is None else f'{self.token}'
        return f'Get({token})'


@dataclass
class FnRef(BinOp):
    def __init__(self, ref=None, parameters=None, op=None, is_lvalue=True):
        assert ref is not None, "Ref not passed to FnRef constructor"
        op = Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex=ref.name or "", loc=ref.location) if op is None else op
        super().__init__(left=ref, op=op, right=parameters, is_lvalue=is_lvalue)
        self.name = ref.name
        if parameters is not None:
            self.count = len(parameters)
        else:
            self.count = 0


@dataclass
class FnCall(FnRef):
    def __init__(self, ref=None, parameters=None, op=None, is_lvalue=True):
        assert ref is not None, "no Ref passed to FnCall constructor"
        op = Token(tid=TK.FUNCTION, tcl=TCL.FUNCTION, lex=ref.name, loc=ref.location) if op is None else op
        super().__init__(ref=ref, op=op, parameters=parameters, is_lvalue=is_lvalue)


@dataclass
class IfThenElse(TernaryOp):
    def __init__(self, test=None, then=None, els=None, is_lvalue=False):
        op = Token(tid=TK.IF, tcl=TCL.BINOP, lex='if', loc=test.token.lexeme)
        super().__init__(op=op, left=test, right=then, mid=els, is_lvalue=is_lvalue)

    @property
    def test(self):
        return self.left

    @property
    def then(self):
        return self.right

    @property
    def els(self):
        return self.middle


@dataclass
class Index(FnCall):
    def __init__(self, ref=None, parameters=None, is_lvalue=True):
        assert ref is not None, "no Ref passed to Index constructor"
        super().__init__(ref=ref, parameters=parameters,
                         op=Token(tid=TK.INDEX, tcl=TCL.BINOP, lex="[", loc=ref.location), is_lvalue=is_lvalue)


@dataclass
class PropRef(BinOp):
    def __init__(self, ref=None, member=None, op=None, is_lvalue=True):
        assert ref is not None, "no Ref passed to PropRef constructor"
        op = Token(tid=TK.REF, tcl=TCL.BINOP, lex=".", loc=ref.location) if op is None else op
        super().__init__(left=ref, op=op, right=member, is_lvalue=is_lvalue)


@dataclass
class Return(UnaryOp):
    """
    Simply a Unary holder of an expression.
    """
    def __init__(self, token, expr):
        super().__init__(token, expr)


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
