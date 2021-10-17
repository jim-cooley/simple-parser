from copy import copy
from tokens import TK, TCL
from lexer import Lexer
from symbols import SymbolTable
from tree import UnaryOp, BinOp, Ident, FnCall, PropRef, PropCall, Seq
from literals import Duration, Float, Int, Percent, Set, Str, Time, Bool
from treedump import DumpTree

# token conversion tables, could be array lookups rather than hashtable, but this is easier to maintain and not large.
_tk2binop = {
    TK.BAR: TK.PIPE,
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
    TK.EXPN: TK.POW,
    TK.COLN: TK.COLN,
    TK.EXCL: TK.NOT,
    TK.AND: TK.AND,
    TK.OR: TK.OR,
    TK.DOT: TK.DOT,
    TK.LTE: TK.LTE,
    TK.GTE: TK.GTE,
    TK.LESS: TK.LESS,
    TK.GTR: TK.GTR,
    TK.NEQ: TK.NEQ,
    TK.EQEQ: TK.ISEQ,  # ==
}

_tk2unop = {
    TK.PLUS: TK.PLUS,  # unary +
    TK.MNUS: TK.NEG,  # unary -
    TK.NOT: TK.NOT,
    TK.EXCL: TK.NOT,  # !
}

_ASSOCIATIVE_OPERATORS = [
    TK.PLUS, TK.MNUS, TK.EQLS, TK.AMPS, TK.EXPN, TK.BAR, TK.AND, TK.OR, TK.DOT, TK.COLN, TK.EQLS
]

_BINARY_TOKENS = [
    TK.STAR, TK.SLSH, TK.GTR2, TK.LSS2, TK.LBAR, TK.RBAR,
    TK.NEQ, TK.EQEQ, TK.LTE, TK.GTE, TK.LESS, TK.GTR
]

_ADDITION_TOKENS = [TK.PLUS, TK.MNUS]

_COMPARISON_TOKENS = [TK.LESS, TK.LTE, TK.GTR, TK.GTE, TK.IN, TK.LBAR, TK.RBAR]

_FLOW_TOKENS = [TK.BAR, TK.GTR2, TK.SEMI, TK.COLN]

_EQUALITY_TEST_TOKENS = [TK.EQEQ, TK.NEQ]

_LOGIC_TOKENS = [TK.AND, TK.OR, TK.AMPS]

_MULTIPLICATION_TOKENS = [TK.SLSH, TK.STAR, TK.EXPN, TK.DOT]

_UNARY_TOKENS = [TK.PLUS, TK.MNUS, TK.NOT, TK.EXCL]

_IDENTIFIER_TYPES = [TCL.KEYWORD, TCL.SERIES, TCL.IDENTIFIER]


class Parser(object):
    def __init__(self, lexer=None, str=None, symtab=None):
        self._symbol_table = (SymbolTable() if lexer is None else lexer.symbols) if symtab is None else symtab
        self._lexer = Lexer(string=str, symtab=self._symbol_table) if lexer is None else lexer
        self._parse_string = str  # which could be none
        self.nodes = []

    # syntactic sugar (use self.peek)
    def __getattr__(self, item):
        if item == 'token':
            return self._lexer.token
        pass

    def _error(self, message):
        loc = self._lexer.tell()
        loc.offset -= 1
        error_text = f'Invalid Syntax: {message}.'
        self._report(error_text, loc)
        raise Exception(error_text)

    def _expected(self, expected, found):
        message = f'Expected {expected}, found {found}'
        self._error(message)

    def _report(self, message, loc):
        carrot = f'\n\n{self._parse_string}\n{"^".rjust(loc.offset)}\n'
        text = f"{carrot}\n{message} at position: {loc.line + 1}:{loc.offset}"
        print(text)

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def peek(self):
        if self.token is None:
            self._lexer.advance()
        return self.token

    # returns current token and advances (!!! UNDONE: needs to be fixed !!!)
    def advance(self):
        return self._lexer.advance()

    # if current token matches
    def check(self, ex_tid):
        return False if self.token.id == TK.EOF else self.token.id == ex_tid

    def expect(self, ex_tid):
        if self.token.id == ex_tid:
            return self.token
        self._expected(expected=f'{ex_tid.name}', found=f'{self.token.id.name}')

    def expect_next(self, ex_tid=None):
        token = self.advance()
        if self.token.id == ex_tid:
            return token
        self._expected(expected=f'{ex_tid.name}', found=f'{self.token.id.name}')

    # match if current token is any of the set.  advance if so.
    def match(self, tk_list):
        tk = self.peek()
        if tk is None or tk.id == TK.EOF:
            return False
        if tk.id in tk_list:
            self.advance()
            return True
        return False

    # skip over the expected current token.
    def skip(self, ex_tid):
        if self.token.id == ex_tid:
            return self.advance()
        self._expected(expected=f'{ex_tid.name}', found=f'{self.token.id.name}')

    # -----------------------------------
    # Recursive Descent Parser States
    # -----------------------------------
    def prime(self):
        node = None
        token = self.peek()
        if token.id == TK.FALSE:
            node = Bool(token, False)
        elif token.id == TK.TRUE:
            node = Bool(token, True)
        elif token.id == TK.NONE:
            node = Set(token, None)
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
        elif token.id == TK.LBRC:
            self.skip(TK.LBRC)
            node = Set(token, Seq(token, self.sequence(TK.COMA)))
            self.skip(TK.RBRC)
        elif token.id == TK.LPRN:
            self.advance()
            node = self.expression()
            self.skip(TK.RPRN)
            return node
        elif token.t_class in _IDENTIFIER_TYPES or token.id == TK.IDNT:
            return self.identifier()
        else:
            return node
        self.advance()
        return node

    # handle unary expressions
    def unary(self):
        op = self.peek()
        if self.match(_UNARY_TOKENS):
            return UnaryOp(op.map(_tk2unop), self.unary())
        node = self.prime()
        if node is not None and node.token.id in [TK.ANY, TK.ALL, TK.NONEOF]:
            node = UnaryOp(node.token, self.unary())
        return node

    def factor(self):
        node = self.unary()
        op = self.token
        while self.match(_MULTIPLICATION_TOKENS):
            node = BinOp(node, op.map(_tk2binop), self.unary())
            op = self.token
        return node

    def term(self):
        node = self.factor()
        op = self.token
        while self.match(_ADDITION_TOKENS):
            node = BinOp(node, op.map(_tk2binop), self.factor())
            op = self.token
        return node

    def comparison(self):
        node = self.term()
        op = self.token
        while self.match(_COMPARISON_TOKENS):
            node = BinOp(node, op.map(_tk2binop), self.term())
            op = self.token
        return node

    def equality(self):
        node = self.comparison()
        op = self.token
        while self.match(_EQUALITY_TEST_TOKENS):
            node = BinOp(node, op.map(_tk2binop), self.comparison())
            op = self.token
        return node

    def logic_expr(self):
        node = self.equality()
        op = self.token
        while self.match(_LOGIC_TOKENS):
            node = BinOp(node, op.map(_tk2binop), self.equality())
            op = self.token
        return node

    def assignment(self):
        node = self.logic_expr()
        op = self.token
        while self.match([TK.EQLS]):
            if node.token.t_class not in _IDENTIFIER_TYPES:
                self._expected(expected='IDENTIFIER', found=f'{node.token.id.name}')
            node = BinOp(left=node, op=op.map(_tk2binop), right=self.logic_expr())
        return node

    def flow(self):
        node = self.assignment()
        op = copy(self.token)  # need a copy or we modify the _lexer's token with op.map()
        if op.id in _FLOW_TOKENS:
            seq = Seq(op.map(_tk2binop), [node])
            while self.match(_FLOW_TOKENS):
                node = self.logic_expr()
                seq.append(node)
            node = seq
        return node

    def expression(self):
        return self.flow()

    def identifier(self):
        tk = self._symbol_table.find_add_symbol(self.peek())
        token = self.advance()
        if token.id == TK.DOT:
            token = self.expect_next(TK.IDNT)
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
            node = self.expression()
            seq.append(node)
            if self.peek().id != sep:
                break
            self.skip(sep)
        return seq

    def parse(self):
        self.nodes = []
        while self._lexer.readable():
            node = self.expression()
            self.nodes.append(node)
        return self.nodes

    @staticmethod
    def print_tree(node):
        dt = DumpTree()
        viz = dt.dump(node)
        for v in viz:
            print(v)
