# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy, deepcopy
from dataclasses import dataclass

from tokens import Token, TCL, TK
from tree import AST, Expression


@dataclass
class Scope:
    def __init__(self, parent_scope=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_scope = parent_scope
        self._symbols = {}

    @property
    def value(self):
        return self._symbols

    @value.setter
    def value(self, value):
        self.token.value += value

    @property
    def name(self):
        if self.token is None or self.token.lexeme is None:
            return ''
        return self.token.lexeme

    def assign(self, token, expr):
        self._find_add(token, expr)

    def define(self, token, expr):
        self._find_add(token, expr)

    def contains(self, token):
        return token.lexeme in self._symbols

    def link(self, scope):
        self.parent_scope = scope
        return self

    def unlink(self):
        self.parent_scope = None
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
            symbol = Ident(copy(token))
            symbol.value = value
            self._symbols[token.lexeme] = symbol
        return symbol

    def find_add_local(self, token, value=None):
        symbol = self.find_local(token)
        if symbol is None:
            symbol = Ident(deepcopy(token))
            symbol.parent_scope = self
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

    def print(self, indent=0):
        spaces = '' if indent < 1 else ' '.ljust(indent * 4)
        for k in self._symbols.keys():
            print(f'{spaces}{k}: {self._symbols[k]}')


@dataclass
class Object(AST, Scope):
    def __init__(self, token=None, value=None, parent=None):
        super().__init__(token=token, value=value, parent=parent, parent_scope=None)
        self.is_lvalue = True

    def format(self):
        tk = self.token
        return f'{tk.value}' if tk.value is not None and tk.value else 'None'


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

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

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
class Flow(Block):
    def __init__(self, token=None, llist=None):
        super().__init__(items=llist)
        token.value = llist
        self.token = token


@dataclass
class Ident(Object):
    def __init__(self, token=None, parent=None):
        super().__init__(token=token, parent=parent)
        self.value = token.lexeme

    def format(self):
        return f'Ident({self.name})'


@dataclass
class Literal(Object):
    def __init__(self, token=None, value=None, parent=None):
        super().__init__(token=token, value=value, parent=parent)
        if token is not None:
            token.t_class = TCL.LITERAL
            self.token.id = token.map2litval().id
        else:
            self.token = Token(tid=TK.OBJECT, tcl=TCL.LITERAL, val=value)


def _dump_symbols(scope):
    print("\n\nsymbols: ")
    idx = 0
    for k in scope._symbols.keys():
        v = scope._symbols[k]
        if type(v).__name__ == 'Ident':
            print(f'{idx:5d}:  {k} : Ident({v.token})')
            idx += 1