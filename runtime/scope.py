# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import deepcopy, copy
from dataclasses import dataclass
from queue import SimpleQueue

from runtime.indexdict import IndexedDict
from runtime.token import Token
from runtime.token_class import TCL
from runtime.token_ids import TK
from runtime.tree import AST, Expression


@dataclass
class Scope:
    def __init__(self, name=None, parent_scope=None, members=None, other=None, hidden=False, **kwargs):
        super().__init__(**kwargs)
        self._hidden = hidden
        self.parent_scope = parent_scope
        if other is not None:
            self.code = copy(other.code)
            self._name = copy(other.name)
            self._fqname = other._fqname
            members = copy(other._members)
        else:
            self.code = None
            self._name = name
            self._fqname = None
        self._members = IndexedDict() if members is None else members

    def __len__(self):
        return len(self._members.keys())

    @property
    def name(self):
        return self._name

    @property
    def qualname(self):
        if self._fqname is None:
            self._fqname = self._calc_fqname()
        return self._fqname

    def members(self):
        return self._members

    def link(self, scope):
        self.parent_scope = scope
        return self

    def unlink(self):
        self.parent_scope = None
        return self

    def update_members(self, other):
        if isinstance(other, Scope):
            self._members.update(other._members)
        else:
            self._members.update(other)

    def from_block(self, block, copy=True):
        if block._members is not None:
            self._members = block._members
            if copy:
                self._members = deepcopy(block._members)
            for s in self._members:
                s.parent_scope = self
        if copy:
            self.code = deepcopy(block.code)
        else:
            self.code = block
        return self

    def assign(self, name, expr):
        sym = self.find(name)
        if sym is None:
            raise ValueError(f'Symbol `{name}` does not exist')
        sym.from_value(expr)
        return sym

    def contains(self, token):
        return token.lexeme in self._members

    def define(self, name=None, value=None, token=None, local=False, update=False):
        """
        Searches for a symbol, defining it if it does not exist.  If a symbol exists in the current scope or parent scopes, then it will
        be found and returned.  The behavior is always to define the symbol in the current scope, 'local' can be used
        to truncate the search for any existing symbols but allocation is always current.
        If the symbol exists, it will not be overwritten, use 'update' to update the value instead.
        :param name: name of symbol to find/define
        :param token: (optional) if present, token will be used instead of name for searching / defining the symbol
        :param value: value to assign if value is created.
        :param local: whether or not parent scopes should be examined while searching for an existing symbol.
        :param update: whether or not an existing value should be overwritten.  This is dangerous if 'local' is not False
        :return: the found / defined / updated symbol
        """
        if token is not None:
            name = token.lexeme
        symbol = self.find(name, local=local)
        if symbol is None or update:
            if symbol is None:
                symbol = Object(name=name, token=token)
            if value is not None:
                if hasattr(symbol, 'token') and hasattr(value, 'token'):
                    if value.token is not None and symbol.token is not None:
                        symbol.token.location = value.token.location
                if hasattr(value, '_members'):
                    symbol._members = deepcopy(value._members)
                if hasattr(value, 'value'):
                    symbol._value = deepcopy(value.value)
                else:
                    symbol._value = deepcopy(value)
            symbol.parent_scope = self
            self._members[name] = symbol
        return symbol

    def redefine(self, name=None, value=None, local=False):
        symbol = self.find(name, local=local)
        if symbol is None:
            return self.define(name=name, value=value, local=local)
        self._members[name] = value
        return value

    def find(self, name=None, token=None, default=None, local=False):
        scope = self
        if token is not None:
            name = token.lexeme
        while scope is not None:
            if scope._members is not None:
                if name in scope._members:
                    return scope._members[name]
            if local:
                break
            scope = scope.parent_scope
        return default

    def _add_symbol(self, tkid, tcl, lex):
        tk = Token(tid=tkid, tcl=tcl, lex=lex, loc=Token.Loc())
        self._members[lex] = tk

    def _add_name(self, name, symbol):
        self._members[name] = symbol

    def _calc_fqname(self):
        if not self._hidden:
            if self._name is None:
                self._fqname = self._name = ''
            elif self.parent_scope is None:
                self._fqname = self._name
            else:
                pname = self.parent_scope._calc_fqname()
                pname = '' if pname is None or pname == '.' else f'{pname}.'
                self._fqname = f'{pname}{self._name}'
        return self._fqname

    def print(self, indent=0):
        spaces = '' if indent < 1 else ' '.ljust(indent * 4)
        for k in self._members.keys():
            print(f'{spaces}{k}: {self._members[k]}')


@dataclass
class Object(AST, Scope):
    def __init__(self, name=None, value=None, members=None, parent=None, token=None, **kwargs):
        if name is None:
            if token is not None and token.lexeme is not None:
                name = token.lexeme  # UNDONE: this is very silly on Literal subclasses (name = 'true')
        super().__init__(name=name, parent_scope=None, value=value, members=members, parent=parent, token=token, **kwargs)
        self.code = None
        self.parameters = None
        self.is_lvalue = True
#       self._calc_fqname()

    def __str__(self):
        if hasattr(self, 'format') is not None:
            return self.format()
        return self.__repr__()

    def __repr__(self):
        return f'{type(self).__name__}({self._value})'

    def from_dict(self, other):
        if isinstance(other, dict) or isinstance(other, IndexedDict):
            self._members.update(other)
            return self
        else:
            raise ValueError("object for assignment is not a dict subclass")

    def from_object(self, other):
        return self.from_block(other)

    def from_value(self, value):
        eval_assignment_dispatch(self, value)
        return self

    def to_dict(self, unbox_values=True):
        d = deepcopy(self._members)
        if unbox_values:
            for k in d.keys():
                v = d[k]
                if hasattr(v, 'value'):
                    v = v._value
                d[k] = v
        return d

    def format(self, brief=True):
        tk = self.token
        if brief:
            v = f'{self._value}' if self._value is not None else 'None'
        else:
            if self.code is not None:
                return f'{self.name}({self.parameters}) = {self.code}'
            else:
                v = f'{self._value}' if self._value is not None else 'None'
        return f'object: {self.name} = {v}'


# -----------------------------------
# Objects
# -----------------------------------
@dataclass
class Block(Expression, Object):
    def __init__(self, name=None, items=None, members=None, loc=None, **kwargs):
        super().__init__(name=name, token=Token.BLOCK(loc), members=members, **kwargs)
        self._items = items if items is not None else []
        self._members = members if members is not None else {}
        self.code = self._items
        self._value = self._items   # UNDONE: ??
        self.is_lvalue = False

    def __len__(self):
        return len(self._items)

    def items(self):
        """
        items is a list of AST 'items' used to construct this block instance.
        """
        return self._items

    def invoke(self, interpreter, args=None):
        pass


@dataclass
class Flow(Block):
    def __init__(self, token=None, items=None):
        super().__init__(items=items)
        token.value = items
        self.from_token(token)

    def invoke(self, interpreter, args=None):
        pass


@dataclass
class FunctionBase(Block):
    def __init__(self, name=None, members=None, closure=None, arity=None, opt=None, defaults=None, parameters=None, other=None, tid=None, loc=None, is_lvalue=True):
        if other is not None:
            name = other.name
            members = other._members
            parameters = other.parameters
            if isinstance(other, FunctionBase):
                defaults = other.defaults
        super().__init__(name=name, members=members, loc=loc)
        self.arity = arity or 0
        self.parent_scope = closure
        self.closure = closure
        self.opt = opt or 0
        self.set_token(tid=tid or TK.IDENT, tcl=TCL.FUNCTION, loc=loc, lex=name)
        self._value = self._items
        self.is_lvalue = is_lvalue
        self.code = None
        self.parameters = parameters
        if defaults is not None:
            if not isinstance(defaults, IndexedDict):
                defaults = IndexedDict(items=defaults)
            if self.arity is None:
                self.arity = len(defaults)
        self.defaults = defaults

    def invoke(self, interpreter, args=None):
        assert False, f'Function {self.name} is not implemented'

    def format(self, brief=True):
        v = f'{self._value}' if self._value is not None else 'None'
        return f'{self.name} = {v}'


def _dump_symbols(scope):
    print("\n\nsymbols: ")
    idx = 0
    q = SimpleQueue()
    q.put(scope)
    while not q.empty():
        s = q.get()
        if s._members is None or len(s._members) == 0:
            continue
        if hasattr(s, 'token'):
            print(f'\nscope: {s.token.lexeme}')
        else:
            print(f'\nglobal scope:')
        for k in s._members.keys():
            v = s._members[k]
            if type(v).__name__ == 'Object':
                q.put(v)
                print(f'{idx:5d}:  `{k}`: {v.qualname} : Object({v.token})')
                idx += 1


