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

    def from_block(self, block):
        self._members = block._members
        for s in self._members.values():
            s.parent_scope = self
        return self

    def assign(self, token, expr):
        sym = self.find(token)
        if sym is None:
            raise ValueError(f'Symbol `{token.lexeme}` does not exist')
        sym.from_value(expr)
        return sym

    def contains(self, token):
        return token.lexeme in self._members

    def define(self, token, expr):
        sym = self._find_add_local(token, expr)
        return sym

    def link(self, scope):
        self.parent_scope = scope
        return self

    def unlink(self):
        self.parent_scope = None
        return self

    def update(self, name, value):
        sym = self.find_update_name(name, value)
        if sym is None:
            raise ValueError(f'Symbol `{name}` does not exist')
        return sym

    def find(self, token, default=None):
        return self.find_name(token.lexeme, default)

    def find_local(self, token, default=None):
        return self.find_local_name(token.lexeme, default)

    def find_add(self, token, value=None):
        symbol = self.find(token)
        if symbol is None:
            symbol = Object(token=copy(token))
            symbol._value = value
            self._members[token.lexeme] = symbol
        return symbol

    def find_name(self, name, default=None):
        scope = self
        while scope is not None:
            if name in scope._members:
                return scope._members[name]
            scope = scope.parent_scope
        return default

    def find_local_name(self, name, default=None):
        if name in self._members:
            return self._members[name]
        return default

    def find_add_local(self, token, value=None):
        symbol = self.find_local(token)
        if symbol is None:
            symbol = Object(token=deepcopy(token))
            symbol.parent_scope = self
            symbol._calc_fqname()
            if getattr(value, '_symbols', False):
                symbol._members = deepcopy(value._members)
                symbol._value = symbol
            else:
                symbol._value = deepcopy(value)
            self._members[token.lexeme] = symbol
        return symbol

    def update_local(self, name, value=None):
        if name in self._members:
            if value is not None:
                sym = self._members[name]
                if hasattr(value, '_name'):
                    value._name = name
                if hasattr(sym, 'token') and hasattr(value, 'token') and sym.token is not None:
                    value.token.location = sym.token.location
            self._members[name] = value
            return self._members[name]
        return None

    def update_name(self, name, value=None):
        scope = self
        while scope is not None:
            if name in scope._members:
                sym = scope._members[name]
                if value is not None:
                    if hasattr(value, '_name'):
                        value._name = name
                    if hasattr(sym, 'token') and sym.token is not None:
                        value.token.location = sym.token.location
                scope._members[name] = value
                return scope._members[name]
            scope = scope.parent_scope
        return None

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
        self.defaults = defaults


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
