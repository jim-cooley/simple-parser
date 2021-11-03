# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy, deepcopy
from dataclasses import dataclass
from queue import Queue, SimpleQueue

from tokens import Token, TCL, TK
from tree import AST, Expression


@dataclass
class Scope:
    def __init__(self, parent_scope=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_scope = parent_scope
        self._symbols = {}

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
            symbol = Object(copy(token))
            symbol.value = value
            self._symbols[token.lexeme] = symbol
        return symbol

    def find_add_local(self, token, value=None):
        symbol = self.find_local(token)
        if symbol is None:
            symbol = Object(deepcopy(token))
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

    @property
    def value(self):
        return self.token.value

    @value.setter
    def value(self, value):
        self.token.value = value

    def format(self):
        tk = self.token
        return f'{tk.lexeme} = ' + (f'{tk.value}' if tk.value is not None else 'None')


# -----------------------------------
# Objects
# -----------------------------------
@dataclass
class Block(Expression, Object):
    def __init__(self, items=None, loc=None):
        op = Token(tid=TK.BLOCK, tcl=TCL.SCOPE, loc=loc)
        super().__init__(token=op, is_lvalue=False)
        self.items = items if items is not None else []


@dataclass
class Flow(Block):
    def __init__(self, token=None,llist=None):
        super().__init__(items=llist)
        token.value = llist
        self.token = token


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
                print(f'{idx:5d}:  {k} : Object({v.token})')
                idx += 1
