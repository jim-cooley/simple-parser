# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy, deepcopy
from dataclasses import dataclass
from queue import SimpleQueue

from tokens import Token, TCL, TK, TK_NONE
from tree import AST, Expression


@dataclass
class Scope:
    def __init__(self, parent_scope=None, name=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_scope = parent_scope
        self._name = name
        self._fqname = self._calc_fqname()
        self._symbols = {}

    def __len__(self):
        return len(self._symbols.keys())

    @property
    def name(self):
        return self._name

    @property
    def qualname(self):
        return self._name if self._fqname is None else self._fqname

    def from_block(self, block):
        self._symbols = block._symbols
        for s in self._symbols.values():
            s.parent_scope = self
            s._calc_fqname()
        return self

    def assign(self, token, expr):
        sym = self.find(token)
        if sym is None:
            raise ValueError(f'Symbol `{token.lexeme}` does not exist')
        sym.from_value(expr)
        return sym

    def contains(self, token):
        return token.lexeme in self._symbols

    def define(self, token, expr):
        sym = self._find_add_local(token, expr)
        sym._calc_qualname()
        return sym

    def link(self, scope):
        self.parent_scope = scope
        self._fqname = self._calc_fqname()
        return self

    def unlink(self):
        self.parent_scope = None
        self._fqname = self._name
        return self

    def find(self, token, default=None):
        scope = self
        while scope is not None:
            if token.lexeme in scope._symbols:
                tk = copy(scope._symbols[token.lexeme])
                tk.location = token.location
                return tk
            scope = scope.parent_scope
        return default

    def find_local(self, token, default=None):
        if token.lexeme in self._symbols:
            return self._symbols[token.lexeme]
        return default

    def find_add(self, token, value=None):
        symbol = self.find(token)
        if symbol is None:
            symbol = Object(copy(token))
            symbol.value = value
            self._symbols[token.lexeme] = symbol
        return symbol

    def find_add_local(self, token, value=None):
        symbol = self.find_local(token)
        if symbol is None:
            symbol = Object(deepcopy(token))
            symbol.parent_scope = self
            symbol._calc_fqname()
            if getattr(value, '_symbols', False):
                symbol._symbols = deepcopy(value._symbols)
                symbol.value = symbol
            else:
                symbol.value = deepcopy(value)
            self._symbols[token.lexeme] = symbol
        return symbol

    def _add_symbol(self, tkid, tcl, lex):
        tk = Token(tid=tkid, tcl=tcl, lex=lex, loc=Token.Loc())
        self._symbols[lex] = tk

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
        for k in self._symbols.keys():
            print(f'{spaces}{k}: {self._symbols[k]}')


@dataclass
class Object(AST, Scope):
    def __init__(self, token=None, value=None, parent=None):
        super().__init__(token=token, value=value, parent=parent, parent_scope=None)
        self.is_lvalue = True
        self.value = token.value
        if self.token is None or self.token.lexeme is None:
            self._name = ''
        else:
            self._name = self.token.lexeme  # UNDONE: this is very silly on Literal subclasses (name = 'true')
            self._calc_fqname()

    def from_object(self, other):
        return self.from_block(other)

    def from_value(self, value):
        eval_assignment_dispatch(self, value)
        return self

    def to_dict(self, unbox_values=True):
        d = deepcopy(self._symbols)
        if unbox_values:
            for k in d.keys():
                v = d[k]
                if getattr(v, 'value', False):
                    v = v.value
                d[k] = v
        return d

    def format(self):
        tk = self.token
        v = f'{tk.value}' if tk.value is not None else 'None'
        return f'{self.qualname} = {v}'


# -----------------------------------
# Objects
# -----------------------------------
@dataclass
class Block(Expression, Object):
    def __init__(self, items=None, loc=None):
        op = Token(tid=TK.BLOCK, tcl=TCL.SCOPE, loc=loc)
        super().__init__(token=op, is_lvalue=False)
        self.items = items if items is not None else []
        self.value = self.items
        self.is_l_value = False

    def __len__(self):
        return len(self.items)


@dataclass
class Flow(Block):
    def __init__(self, token=None, llist=None):
        super().__init__(items=llist)
        token.value = llist
        self.token = token


def _dump_symbols(scope):
    print("\n\nsymbols: ")
    idx = 0
    q = SimpleQueue()
    q.put(scope)
    while not q.empty():
        s = q.get()
        if s._symbols is None or len(s._symbols) == 0:
            continue
        if getattr(s, 'token', False):
            print(f'\nscope: {s.token.lexeme}')
        else:
            print(f'\nglobal scope:')
        for k in s._symbols.keys():
            v = s._symbols[k]
            if type(v).__name__ == 'Object':
                q.put(v)
                print(f'{idx:5d}:  `{k}`: {v.qualname} : Object({v.token})')
                idx += 1
