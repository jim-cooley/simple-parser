# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy, deepcopy
from dataclasses import dataclass
from queue import SimpleQueue

from indexed_dict import IndexedDict
from tokens import Token, TCL, TK
from tree import AST, Expression


@dataclass
class Scope:
    def __init__(self, parent_scope=None, name=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_scope = parent_scope
        self._name = name
        self._fqname = None
        self._members = {}

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

    def link(self, scope):
        self.parent_scope = scope
        return self

    def unlink(self):
        self.parent_scope = None
        return self

    def update_members(self, other):
        self._members.update(other)

    def from_block(self, block):
        self._members = block._members
        for s in self._members.values():
            s.parent_scope = self
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
        if symbol is None and not update:
            if symbol is None:
                symbol = Object(name=name, token=token)
            if value is not None:
                if hasattr(symbol, 'token') and hasattr(value, 'token'):
                    if value.token is not None and symbol.token is not None:
                        symbol.token.location = value.token.location
                if hasattr(value, '_members'):
                    symbol._members = deepcopy(value._members)
                    symbol._value = deepcopy(value.value)
                else:
                    if hasattr(value, 'value'):
                        symbol._value = deepcopy(value.value)
                    else:
                        symbol._value = deepcopy(value)
            symbol.parent_scope = self
            symbol._calc_fqname()
            self._members[name] = symbol
        return symbol

    def find(self, name=None, token=None, default=None, local=False):
        scope = self
        if token is not None:
            name = token.lexeme
        while scope is not None:
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
    def __init__(self, name=None, value=None, token=None, parent=None):
        if name is None:
            if token is not None and token.lexeme is not None:
                name = token.lexeme  # UNDONE: this is very silly on Literal subclasses (name = 'true')
        super().__init__(value=value, token=token, parent=parent, name=name, parent_scope=None)
        self.code = None
        self.parameters = None
        self.is_lvalue = True
        self._calc_fqname()

    def __str__(self):
        if getattr(self, 'format', None) is not None:
            return self.format()
        return self.__repr__()

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

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
                if getattr(v, 'value', False):
                    v = v._value
                d[k] = v
        return d

    def format(self):
        tk = self.token
        if self.code is not None:
            return f'{self.name}({self.parameters}) = {self.code}'
        else:
            v = f'{tk.value}' if tk.value is not None else 'None'
            return f'{self.name}({v})'


# -----------------------------------
# Objects
# -----------------------------------
@dataclass
class Block(Expression, Object):
    def __init__(self, name=None, items=None, loc=None, is_lvalue=False):
        op = Token(tid=TK.BLOCK, tcl=TCL.SCOPE, loc=loc)
        super().__init__(token=op, name=name)
        self.items = items if items is not None else []
        self._value = self.items
        self.is_lvalue = False

    def __len__(self):
        return len(self.items)


@dataclass
class Flow(Block):
    def __init__(self, token=None, items=None):
        super().__init__(items=items)
        token._value = items
        self.token = token


@dataclass
class Function(Block):
    def __init__(self, name=None, members=None, defaults=None, tid=None, loc=None, is_lvalue=True):
        super().__init__(name=name, items=members, loc=loc)
        token = Token(tid=tid or TK.IDNT, tcl=TCL.FUNCTION, lex=name, loc=loc)
        self.token = token
        self._value = self.items
        self.is_lvalue = is_lvalue
        self.code = None
        self.parameters = None
        self.defaults = None
        if defaults is not None:
            if not isinstance(defaults, IndexedDict):
                defaults = IndexedDict(items=defaults)
            self.defaults = defaults

    def count(self):
        """
        Parameter count.  Defines the Function's signature
        """
        return len(self.defaults)


@dataclass
class IntrinsicFunction(Function):
    def __init__(self, name=None, members=None, defaults=None, tid=None, loc=None, is_lvalue=False):
        super().__init__(name=name, members=members, defaults=defaults, tid=tid, loc=loc, is_lvalue=is_lvalue)
        self.token.is_reserved = True


def _dump_symbols(scope):
    print("\n\nsymbols: ")
    idx = 0
    q = SimpleQueue()
    q.put(scope)
    while not q.empty():
        s = q.get()
        if s._members is None or len(s._members) == 0:
            continue
        if getattr(s, 'token', False):
            print(f'\nscope: {s.token.lexeme}')
        else:
            print(f'\nglobal scope:')
        for k in s._members.keys():
            v = s._members[k]
            if type(v).__name__ == 'Object':
                q.put(v)
                print(f'{idx:5d}:  `{k}`: {v.qualname} : Object({v.token})')
                idx += 1
