# abstract syntax trees:
from dataclasses import dataclass

from runtime.token_data import EXPRESSION_TOKENS, _tk2type, _tk2glyph
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

    def __init__(self, token=None, tid=None, value=None, parent=None, loc=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        if token is not None:
            self.tid = token.id
            self.location = token.location
            self.lexeme = token.lexeme
        else:
            self.tid = tid
            self.lexeme = None
            self.location = loc
        self._value = value
        if value is None and token is not None:
            self._value = token.value

    def __str__(self):
        if hasattr(self, 'format') is not None:
            return self.format()
        return self.__repr__()

    @property
    def token(self):
        if self.tid:
            return Token(tid=self.tid, tcl=_tk2type[self.tid], lex=self.lexeme, loc=self.location)
        else:
            return Token.NONE(self.location)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # token fields are split out for the AST.  tcl is the first dropped,
    # as well as is_reserved which is replaced with is_lvalue.  This is to ease the transition.
    def set_token(self, tid=None, tcl=None, loc=None, lex=None, val=None):
        self.tid = tid or self.tid
        self.location = loc or self.location
        self.lexeme = lex or self.lexeme
        self._value = val or self.value

    def from_token(self, token):
        if token is not None:
            self.tid = token.id
            self.location = token.location
            self.lexeme = token.lexeme
            self._value = token.value


# a compound node containing a sequence of 'items'
@dataclass
class ASTCompound(AST):
    def __init__(self, token=None, tid=None, value=None, parent=None, **kwargs):
        super().__init__(token=token, tid=tid, value=value, parent=parent, **kwargs)
        self._items = []

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = int(value)

    def __len__(self):
        return len(self._items)

    @property
    def last(self):
        return self._items[len(self._items) - 1]

    @last.setter
    def last(self, value):
        self._items[len(self._items) - 1] = value

    def append(self, item):
        self._items.append(item)

    def items(self):    # UNDONE: should be iterator
        return self._items

    def len(self):
        return len(self._items)

    def values(self):
        return self._items

    def format(self, brief=True):
        if self.value is None:
            return '{}'
        else:
            if not brief:
                fstr = ''
                max = (len(self._items) - 1)
                if max > 0:
                    for idx in range(0, len(self.value)):
                        fstr += f'{self._items[idx]}'
                        fstr += ',' if idx < max else ''
                else:
                    fstr = f'{self._value}'
            else:
                fstr = f'count={len(self.value)}'
            return '{' + f'{fstr}' + '}'


@dataclass
class Expression(ASTCompound):
    def __init__(self, token=None, tid=None, value=None, parent=None, is_lvalue=True, **kwargs):
        super().__init__(token=token, tid=tid, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


@dataclass
class Statement(ASTCompound):
    def __init__(self, token=None, value=None, parent=None, is_lvalue=True, **kwargs):
        super().__init__(token=token, value=value, parent=parent, **kwargs)
        self.is_lvalue = is_lvalue


# -----------------------------------
# Base Nodes
# -----------------------------------
@dataclass
class Assign(Expression):
    def __init__(self, left=None, op=None, right=None, is_lvalue=None):
        super().__init__(token=op, tid=TK.ASSIGN, is_lvalue=False if is_lvalue is None else is_lvalue)
        self.left = left
        self.right = right
        self.tid = self.op = TK.ASSIGN  # UNDONE: this definition of 'op' is incompatible with BinOp and others
        if right is not None:
            right.parent = self

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'Assign({self.op.name}: {lval}, {rval})'


@dataclass
class BinOp(Expression):
    def __init__(self, left=None, op=None, right=None, is_lvalue=None):
        super().__init__(token=op, is_lvalue=True if is_lvalue is None else is_lvalue)
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

    def __str__(self):
        return f'{type(self).__name__}(TK.{self.op.name}, \'{self.token.lexeme}\')'

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'BinOp(TK.{self.op.name}: {lval}, {rval})'


@dataclass
class Define(Assign):
    """
    Base of the Definition Nodes.  In its simplest form, it Defines a symbol (variable).
    The symbol need not be defined when called.
    """

    def __init__(self, left=None, op=None, right=None, is_lvalue=None):
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
        is_lvalue = False
        if op is not None:
            if op.id in [TK.COLN, TK.TUPLE]:
                is_lvalue = is_lvalue
            op.remap2binop().remap(TK.ASSIGN, TK.DEFINE)
        super().__init__(left=left, op=op, right=right, is_lvalue=is_lvalue)
        if right is not None:
            self.is_lvalue = right.is_lvalue
        if op is not None:
            self.tid = self.op = op.id
        else:
            self.tid = self.op = TK.DEFINE

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'Define(TK.{self.op.name}: {lval}, {rval})'


# holds a reference
class Ref(Expression):
    def __init__(self, token, name=None, is_lvalue=True):
        super().__init__(token=token, is_lvalue=is_lvalue)
        self.from_token(token)
        self.name = name or token.lexeme
        if token.is_reserved:
            self.is_lvalue = False

    def to_get(self):
        get = Get(self.token)
        get.parent = self.parent
        return get

    def format(self, brief=True):
        return f'Ref({_tk_name(self.token)}: \'{self.name}\')'


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

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'Apply(TK.{self.op.name}: {lval}, {rval})'


@dataclass
class ApplyChainProd(Apply):
    def __init__(self, left, tid=None, lex=None, loc=None, is_lvalue=False):
        op = Token.APPLY(lex=lex or ">>", loc=loc)
        op.id = tid or TK.APPLY
        super().__init__(left=left, op=op, is_lvalue=is_lvalue)

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'ApplyChainProd(TK.{self.op.name}: {lval}, {rval})'


@dataclass
class Combine(Define):
    def __init__(self, left=None, op=None, right=None, loc=None):
        super().__init__(left=left, op=op, right=right, is_lvalue=True)
        self.op = TK.COMBINE
        if loc is not None:
            self.location = loc


@dataclass
class DefineFn(Define):  # left = FnRef, op=TK, plist, right = Block
    def __init__(self, left=None, op=None, right=None, args=None):
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

    def format(self, brief=True):
        left = self.left
        right = self.right
        args = self.args
        lval = "None"
        rval = "None"
        aval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        if args is not None:
            if hasattr(args, 'format'):
                aval = args.format(brief=brief)
        return f'DefineFn(TK.{self.op.name}: {lval}(a={aval}) = {rval})'


# value takes on defined range during iteration
@dataclass
class DefineVar(Define):
    def __init__(self, left=None, op=None, right=None, is_lvalue=None):
        super().__init__(left=left, op=op, right=right, is_lvalue=False if is_lvalue is None else is_lvalue)

    def format(self, brief=True):
        left = self.left
        right = self.right
        lval = "None"
        rval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        return f'DefineVar(TK.{self.op.name}: {lval}, {rval})'


# value takes on defined range during iteration, and is evaluated each time
@dataclass
class DefineVarFn(DefineVar):
    def __init__(self, left=None, op=None, right=None, args=None):
        super().__init__(left=left, op=op, right=right, is_lvalue=False)
        self.args = args

    def format(self, brief=True):
        left = self.left
        right = self.right
        args = self.args
        lval = "None"
        rval = "None"
        aval = "None"
        if left is not None:
            if hasattr(left, 'format'):
                lval = left.format(brief=brief)
        if right is not None:
            if hasattr(right, 'format'):
                rval = right.format(brief=brief)
        if args is not None:
            if hasattr(args, 'format'):
                aval = args.format(brief=brief)
        return f'DefineVarFn({self.op}: {lval}(a={aval}) = {rval})'


# dereferences to value
class Get(Ref):
    def __init__(self, token, name=None, is_lvalue=True):
        super().__init__(token=token, name=name, is_lvalue=is_lvalue)

    def to_ref(self):
        ref = Ref(self.token)
        ref.parent = self.parent
        return ref

    def get(self):
        return self._value

    def format(self, brief=True):
        token = 'None'
        if self.token is not None:
            if brief:
                token = f'{self.token.lexeme}'
            else:
                token = f'{self.token}'
        return f'Get({token})'


@dataclass
class FnRef(BinOp):
    def __init__(self, ref=None, parameters=None, op=None, is_lvalue=True):
        assert ref is not None, "Ref not passed to FnRef constructor"
        op = Token.FUNCTION(name=ref.name or "", loc=ref.location) if op is None else op
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
        op = Token.FNCALL(name=ref.name, loc=ref.location) if op is None else op
        super().__init__(ref=ref, op=op, parameters=parameters, is_lvalue=is_lvalue)
        self.ref = ref  # for convenience


@dataclass
class Generate(Expression):
    """
    A Generator is a node in the AST that generates a runtime object.  Productions currently supported are:
    1) Blocks
    2) Lists
    3) Sets
    4) Series
    5) DataFrames
    """
    def __init__(self, target=None, parameters=None, loc=None, is_lvalue=True):
        """
        :param name: Expression that evaluates to 'name'
        :param target: Target token-id
        :param parameters: List of items for the generator to operate on
        :param loc: Token location
        :param is_lvalue: Whether or not this can appear on the Left-Hand-Side of an expression
        """
        super().__init__(token=Token.GEN(loc=loc), is_lvalue=is_lvalue)
        self._items = parameters or []
        self.target = target    # target type (tid)

    def format(self, brief=True):
        if self._items is None:
            return f'[]:{_tk2glyph[self.target]}'
        else:
            if not brief:
                fstr = ''
                max = (len(self._items)-1)
                for idx in range(0, len(self._items)):
                    fstr += f'{self._items[idx]}'
                    fstr += ',' if idx < max else ''
            else:
                fstr = f'count={len(self._items) - 1}'
            return '[' + f'{fstr}' + f']:{_tk2glyph[self.target]}'


@dataclass
class IfThenElse(TernaryOp):
    def __init__(self, test=None, then=None, els=None, is_lvalue=False):
        op = Token.IF(loc=test.token.lexeme)
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
        super().__init__(ref=ref, parameters=parameters, op=Token.SUBSCRIPT(loc=ref.location), is_lvalue=is_lvalue)


@dataclass
class PropRef(BinOp):
    def __init__(self, ref=None, member=None, op=None, is_lvalue=True):
        assert ref is not None, "no Ref passed to PropRef constructor"
        op = Token.REF(loc=ref.location) if op is None else op
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


def _tk_name(token):
    _tn = 'None'
    if token is not None:
        _tn = f'{token.id.name}' if hasattr(token.id, "name") else f'{token.id}, '
    return f'TK.{_tn}'


def _format_token(token):
    _tn = f'.{token.id.name}(' if hasattr(token.id, "name") else f'({token.id}, '
    _tv = 'None' if token.value is None else f'{token.value}'
    _tl = f'\'{token.lexeme}\'' if token.lexeme is not None else 'None'
    if _tl == '\'\n\'':
        _tl = "'\\n'"
    return f'{_tk_name(token)}({_tl}, v={_tv})'
