from tokens import TK, TCL
from lexer import Lexer
from symbols import SymbolTable
from tree import UnaryOp, Int, BinOp, Ident, FnCall, PropRef, PropCall, Duration, Time, Seq, Str, Set, Float, Percent
from treedump import DumpTree

# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.STAR: TK.MUL,
    TK.SLSH: TK.DIV,
    TK.PLUS: TK.ADD,
    TK.MNUS: TK.SUB,
    TK.EQLS: TK.ASSIGN,
    TK.GTR2: TK.APPLY,
    TK.LSS2: TK.LSS2,
    TK.LBAR: TK.FALL_BELOW,
    TK.RBAR: TK.RISE_ABOVE,
    TK.AMPS: TK.AND,
    TK.EXPN: TK.EXPN,
    TK.COLN: TK.COLN,
    TK.BAR: TK.OR,
    TK.AND: TK.AND,
    TK.OR: TK.OR,
    TK.DOT: TK.DOT,
    TK.LTE: TK.LTE,
    TK.GTE: TK.GTE,
    TK.LESS: TK.LESS,
    TK.GTR: TK.GTR,
    TK.NEQ: TK.NEQ,
    TK.EQEQ: TK.ISEQ,   # ==
}

_tk2unop = {
    TK.PLUS: TK.PLUS,   # unary +
    TK.MNUS: TK.NEG,    # unary -
    TK.NOT: TK.NOT,
    TK.EXCL: TK.NOT,    # !
}

_ASSOCIATIVE_OPERATORS = [
    TK.PLUS, TK.MNUS, TK.EQLS, TK.AMPS, TK.EXPN, TK.BAR, TK.AND, TK.OR, TK.DOT, TK.COLN, TK.EQLS
]

_BINARY_OPERATORS = [
    TK.STAR, TK.SLSH, TK.GTR2, TK.LSS2, TK.LBAR, TK.RBAR,
    TK.NEQ, TK.EQEQ, TK.LTE, TK.GTE, TK.LESS, TK.GTR
]

_UNARY_OPERATORS = [
    TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL
]

_IDENTIFIER_TYPES = [
    TCL.KEYWORD, TCL.SERIES, TCL.IDENTIFIER
]


class Parser(object):
    def __init__(self, lexer=None, str=None, symtab=None):
        self._symbol_table = (SymbolTable() if lexer is None else lexer.symbols) if symtab is None else symtab
        self._lexer = Lexer(string=str, symtab=self._symbol_table) if lexer is None else lexer
        self._parse_string = str # which could be none
        self.nodes = []

    # syntactic sugar (use self.peek)
    def __getattr__(self, item):
        if item == 'token':
            return self._lexer.token
        pass

    def _error(self, message):
        loc = self._lexer.tell()
        loc.offset -= 1
        error_text = f"Invalid Syntax: {message}"
        self._report(error_text, loc)
        raise Exception(error_text)

    def _report(self, message, loc):
        carrot = f'\n\n{self._parse_string}\n{"^".rjust(loc.offset)}\n'
        text = f"{carrot}\n{message} at position: {loc.line+1}:{loc.offset}"
        print(text)

    def has_more(self):
        return True if self.token is None else self.token.id != TK.EOF

    # returns current token and advances (!!! UNDONE: needs to be fixed !!!)
    def advance(self):
        return self._lexer.advance()

    # if current token matches
    def check(self, ex_tid):
        return False if self.token.id == TK.EOF else self.token.id == ex_tid

    def check_next(self, ex_tid=None):
        token = self.advance()
        if self.token.id == ex_tid:
            return token
        self._error(f'Expected {ex_tid.name}, found {self.token.id.name}')

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def peek(self):
        if self.token is None:
            self._lexer.advance()
        return self.token

    # skip over the expected current token.
    def skip(self, ex_tid):
        if self.token.id == ex_tid:
            return self.advance()
        self._error(f'Expected {ex_tid.name}, found {self.token.id.name}')

    # fetch new token and see that it matches
    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN"""
        token = self.peek()
        if token.t_class not in _IDENTIFIER_TYPES and token.id != TK.IDNT:
            self.advance()
            if token.id in _UNARY_OPERATORS:  # Unary operators
                token.id = _tk2unop[token.id]
                node = UnaryOp(token, self.factor())
            elif token.id == TK.INT:
                node = Int(token)
            elif token.id == TK.FLOT:
                node = Float(token)
            elif token.id == TK.PCT:
                node = Percent(token)
            elif token.id == TK.DUR:
                node = Duration(token)
            elif token.id == TK.TIME:
                node = Time(token)
            elif token.id == TK.QUOT:
                node = Str(token)
            elif token.id == TK.LPRN:
                node = self.expr()
                self.skip(TK.RPRN)
            elif token.id == TK.LBRC:
                node = Set(token, Seq(token, self.sequence(TK.COMA)))
            elif token.id == TK.LBRK:
                node = self.expr()
                self.skip(TK.RBRK)
            else:
                node = None
        else:
            node = self.identifier()
        return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        token = self.peek()
        if token.id in _BINARY_OPERATORS:
            while token.id in _BINARY_OPERATORS:
                self.advance()
                token.id = _tk2binop[token.id]
                node = BinOp(left=node, token=token, right=self.factor())
                token = self.peek()
#        elif token.id == TK.IDNT:
#            val = self.token.value
#            if val in LOGICAL_OPERATORS:    # replace with sym lookup / type
#                token = self.token
#                self.skip(token.id)
#                node = BinOp(left=node, token=token, right=self.factor())
        return node

    def identifier(self):
        tk = self._symbol_table.find_add_symbol(self.peek())
        token = self.advance()
        if token.id == TK.DOT:
            token = self.check_next(TK.IDNT)
            node = PropRef(tk, self.identifier())
            if token.id == TK.LPRN:
                node = PropCall(tk, node.member, self.plist())
        elif token.id == TK.LPRN:
            node = FnCall(tk, self.plist())
        else:
            node = Ident(tk)
        return node

    def plist(self):
        """( EXPR ',' ... )"""
        seq = []
        token = self.peek()
        self.skip(TK.LPRN)
        token.t_class = TCL.LIST
        token.id = TK.PARAMETER_LIST
        if self.peek().id != TK.RPRN:
            seq = self.sequence(TK.COMA)
        self.skip(TK.RPRN)
        return Seq(token, seq)

    def sequence(self, sep, node=None):
        """EXPR <sep> EXPR <sep> ..."""
        seq = [] if node is None else [node]
        while True:
            node = self.expr()
            seq.append(node)
            if self.peek().id != sep:
                break
            self.skip(sep)
        return seq

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        """
        node = self.term()
        while self.token.id in _ASSOCIATIVE_OPERATORS:
            token = self.token
            if token.id == TK.BAR:
                self.skip(TK.BAR)
                token.id = TK.PIPE
                token.t_class = TCL.LIST
                node = Seq(token, self.sequence(TK.BAR, node))
            elif token.id == TK.COLN:
                token.id = _tk2binop[token.id]
                self.advance()
                if self.token.id == TK.LPRN:
                    node = BinOp(left=node, token=token, right=self.plist())
                else:
                    node = BinOp(left=node, token=token, right=self.term())
            else:
                self.advance()
                token.id = _tk2binop[token.id]
                node = BinOp(left=node, token=token, right=self.term())
        return node

    def parse(self):
        self.nodes = []
        while self._lexer.readable():
            node = self.expr()
            self.nodes.append(node)
        return self.nodes

    @staticmethod
    def print_tree(node):
        dt = DumpTree()
        viz = dt.dump(node)
        for v in viz:
            print(v)
