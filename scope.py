# one of javascript's interesting things is that a Scope object is an Object.
# in our case 'Set' represents that basic Object, but we make this
# inherit from AST so that we can see where this goes.
from copy import copy
from dataclasses import dataclass

from tokens import Token
from tree import AST


@dataclass
class Scope(AST):
    parent = None
    _symbols = {}

    def __init__(self, parent=None):
        self.parent = parent

    def __getitem__(self, key):
        return self.find(key)

    def __setitem__(self, key, value):
        self.define(key, value)

    def __contains__(self, key):
        return self.contains(key)

    def assign(self, token, expr):
        self._find_add(token, expr)

    def define(self, token, expr):
        self._find_add(token, expr)

    def contains(self, token):
        return token.lexeme in self._symbols

    def find(self, token, default=None):
        scope = self
        while scope is not None:
            if token.lexeme in scope._symbols:
                return scope._symbols[token.lexeme]
            scope = scope.parent
        return default

    def find_local(self, token, default=None):
        if token.lexeme in self._symbols:
            return self._symbols[token.lexeme]
        return default

    def _find_add(self, token, value):
        symbol = self.find(token)
        if symbol is None:
            symbol = copy(token)
            self._symbols[token.lexeme] = value
        return symbol

    def _add_symbol(self, tkid, tcl, lex):
        tk = Token(tid=tkid, tcl=tcl, lex=lex, loc=Token.Loc())
        self._symbols[lex] = tk

    def print(self, indent=0):
        spaces = '' if indent < 1 else ' '.ljust(indent * 4)
        for k in self._symbols.keys():
            print(f'{spaces}{k}: {self._symbols[k]}')
