from copy import copy
from tokens import TK, TCL, _ADDITION_TOKENS, _COMPARISON_TOKENS, _FLOW_TOKENS, \
    _EQUALITY_TEST_TOKENS, _LOGIC_TOKENS, _MULTIPLICATION_TOKENS, _UNARY_TOKENS, _IDENTIFIER_TYPES
from lexer import Lexer
from symbols import SymbolTable
from tree import UnaryOp, BinOp, Ident, FnCall, PropRef, PropCall, Seq
from literals import Duration, Float, Int, Percent, Set, Str, Time, Bool
from treedump import DumpTree


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

    # skip over the expected current token.
    def expect(self, ex_tid):
        if self.token.id == ex_tid:
            return self.advance()
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

    # -----------------------------------
    # Parser entry point
    # -----------------------------------
    def parse(self):
        self.nodes = []
        while self._lexer.readable():
            node = self.expression()
            self.nodes.append(node)
        return self.nodes

    # -----------------------------------
    # Recursive Descent Parser States
    # -----------------------------------
    def expression(self):
        node = self.flow()
        op = self.token
        if op.id == TK.SEMI:
            self.advance()
        return node

    def flow(self):
        node = self.set_parameters()
        op = copy(self.token)  # need a copy or we modify the _lexer's token with op.map()
        while op.id in _FLOW_TOKENS:
            sep = op.id
            seq = Seq(op.map2binop(), [node])
            while self.match([sep]):
                node = self.set_parameters()
                seq.append(node)
            node = seq
            op = copy(self.token)
        return node

    def set_parameters(self):
        node = self.assignment()
        op = self.token
        while self.match([TK.COLN]):
            node = BinOp(node, op.map2binop(), self.assignment())
            op = self.token
        return node

    def assignment(self):
        node = self.logic_expr()
        op = self.token
        while self.match([TK.EQLS, TK.ASSIGN]):
            if node.token.t_class not in _IDENTIFIER_TYPES:
                self._expected(expected='IDENTIFIER', found=f'{node.token.id.name}')
            node = BinOp(left=node, op=op.map2binop(), right=self.assignment())
        return node

    def logic_expr(self):
        node = self.equality()
        op = self.token
        while self.match(_LOGIC_TOKENS):
            node = BinOp(node, op.map2binop(), self.equality())
            op = self.token
        return node

    def equality(self):
        node = self.comparison()
        op = self.token
        while self.match(_EQUALITY_TEST_TOKENS):
            node = BinOp(node, op.map2binop(), self.comparison())
            op = self.token
        return node

    def comparison(self):
        node = self.term()
        op = self.token
        while self.match(_COMPARISON_TOKENS):
            node = BinOp(node, op.map2binop(), self.term())
            op = self.token
        return node

    def term(self):
        node = self.factor()
        op = self.token
        while self.match(_ADDITION_TOKENS):
            node = BinOp(node, op.map2binop(), self.factor())
            op = self.token
        return node

    def factor(self):
        node = self.unary()
        op = self.token
        while self.match(_MULTIPLICATION_TOKENS):
            node = BinOp(node, op.map2binop(), self.unary())
            op = self.token
        return node

    def unary(self):
        op = self.peek()
        if self.match(_UNARY_TOKENS):
            return UnaryOp(op.map2unop(), self.unary())
        node = self.prime()
        if node is not None and node.token.id in [TK.ANY, TK.ALL, TK.NONEOF]:
            node = UnaryOp(node.token, self.unary())
        return node

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
            self.expect(TK.LBRC)
            node = Set(token, Seq(token, self.sequence(TK.COMA)))
            self.expect(TK.RBRC)
            return node
        elif token.id == TK.LPRN:
            self.advance()
            node = self.expression()
            self.expect(TK.RPRN)
            return node
        elif token.t_class in _IDENTIFIER_TYPES or token.id == TK.IDNT:
            return self.identifier()
        else:
            return node
        self.advance()
        return node

    # -----------------------------------
    # Helpers
    # -----------------------------------
    def identifier(self):
        """
        identifier | identifier ( plist ) | identifier . identifier
        """
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
        self.expect(TK.LPRN)
        token.t_class = TCL.LIST
        token.id = TK.PARAMETER_LIST
        if self.peek().id != TK.RPRN:
            seq = self.sequence(TK.COMA)
        self.expect(TK.RPRN)
        return Seq(token, seq)

    def sequence(self, sep, node=None):
        """EXPR <sep> EXPR <sep> ..."""
        seq = [] if node is None else [node]
        while True:
            node = self.expression()
            seq.append(node)
            if self.peek().id != sep:
                break
            self.expect(sep)
        return seq

    @staticmethod
    def print_tree(node):
        dt = DumpTree()
        viz = dt.dump(node)
        for v in viz:
            print(v)
