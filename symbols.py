# token / symbol types
import copy
from dataclasses import dataclass
from tokens import TCL, TK, Token, _tk2type

_KEYWORDS = [
    (TK.BUY, TCL.KEYWORD, "buy"),
    (TK.SELL, TCL.KEYWORD, "sell"),
    (TK.SIGNAL, TCL.KEYWORD, "signal"),
    (TK.IDNT, TCL.DATASET, "open"),
    (TK.IDNT, TCL.DATASET, "close"),
    (TK.IDNT, TCL.DATASET, "high"),
    (TK.IDNT, TCL.DATASET, "low"),
    (TK.IDNT, TCL.FUNCTION, "sma"),
    (TK.IDNT, TCL.FUNCTION, "ema"),
    (TK.AND, TCL.LOGICAL, 'and'),
    (TK.OR, TCL.LOGICAL, 'or'),
    (TK.NOT, TCL.UNARY, 'not'),
    (TK.IN, TCL.BINOP, 'in'),
    (TK.ANY, TCL.KEYWORD, 'any'),
    (TK.ALL, TCL.KEYWORD, 'all'),
    (TK.NONEOF, TCL.KEYWORD, 'none'),
#   (TK.NONE, TCL.KEYWORD, 'none'),
    (TK.TRUE, TCL.KEYWORD, 'true'),
    (TK.FALSE, TCL.KEYWORD, 'false'),
    (TK.NONE, TCL.KEYWORD, 'None'),
    (TK.TRUE, TCL.KEYWORD, 'True'),
    (TK.FALSE, TCL.KEYWORD, 'False'),
    (TK.DEFINE, TCL.UNARY, 'def'),
]

_FUNCTIONS = [
    (TK.IDNT, TCL.KEYWORD, 'apply'),
    (TK.IDNT, TCL.KEYWORD, 'columns'),
    (TK.IDNT, TCL.KEYWORD, 'expr'),
    (TK.IDNT, TCL.KEYWORD, 'fillempty'),
    (TK.IDNT, TCL.KEYWORD, 'select')
]


@dataclass
class SymbolTable:
    def __init__(self):
        self._symbolTable = {}          # find token by 'value'
        self._symbolTypeTable = {}      # find all tokens of given type
        self._symbolId = TK.LAST
        self.register_keywords()

    def next_token_id(self):
        self._symbolId += 1
        return self._symbolId

    def get_instances_of_type(self, typ):
        return None if type not in self._symbolTypeTable else self._symbolTypeTable[typ]

    def add_symbol(self, id, typ, lex, prop=None):
        id = id if id >= 0 else self.next_token_id()
        if lex not in self._symbolTable:  # add
            s = Token(id, typ, lex, "", prop)
            typ = TCL.IDENTIFIER if typ is None else typ
            if typ != TCL.LITERAL:
                self._symbolTable[lex] = s
            self.add_token_class(s)
        else:                               # update
            s = self._symbolTable[lex]
            s.id = id if id is not None else s.id
            s.name = typ if typ is not None else s.name
            s.lexeme = lex if lex is not None else s.lexeme
            if prop is not None:
                s.properties.add(prop)
        return s

    def add_token_class(self, token):
        te = [] if token.t_class not in self._symbolTypeTable else self._symbolTypeTable[token.t_class]
        te.append(token)
        self._symbolTypeTable[token.t_class] = te

    def define_symbol(self, token, expr):
        self.find_add_symbol(token)
        self._symbolTable[token.lexeme] = expr

    def find_symbol(self, token):
        if token.lexeme in self._symbolTable:
            return self._symbolTable[token.lexeme]
        return None

    def find_add_symbol(self, token):
        symbol = self.find_symbol(token)
        if symbol is None:
            symbol = self.add_symbol(token.id, token.t_class, token.lexeme, token.properties)
            symbol.location = copy.copy(token.location)
        return symbol

    def find_symbol_by_type(self, token, typ):
        if token.lexeme in self._symbolTable:
            symbol = self._symbolTable[token.lexeme]
            return symbol if symbol.name == typ else None
        return None

    def get_tokentype(self, token, default=TCL.NONE):
        if token.id in self._symbolTable:
            tk = self._symbolTable[token.id]
            return tk.t_class
        return default

    def register_keywords(self, keywords=_KEYWORDS):
        for (tkid, typ, val) in keywords:
            self.add_symbol(tkid, typ, val)

    # this is for type classification for non-identifiers.  the set is small, we insert the tid into the sym table.
    def register_token_types(self, tokens=_tk2type):
        for (tid, tt) in tokens.items():
            self.add_symbol(tid, tt, tid)

    def print(self, indent=0):
        _print_table(self._symbolTable, indent)

    def print_types(self, indent=0):
        for k in self._symbolTypeTable.keys():
            _print_tcl_list(k, self._symbolTypeTable[k], indent)


def _print_tcl_list(tcl, table, indent):
    spaces = '' if indent < 1 else ' '.ljust(indent * 4)
    print(f'{spaces}TCL.{TCL(tcl).name}: {table}')


def _print_table(table, indent):
    spaces = '' if indent < 1 else ' '.ljust(indent * 4)
    for k in table.keys():
        print(f'{spaces}{k}: {table[k]}')
