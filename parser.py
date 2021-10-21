from copy import copy
from dataclasses import dataclass

from exceptions import _expected
from scope import Scope, load_keywords
from tokens import TK, TCL, _ADDITION_TOKENS, _COMPARISON_TOKENS, _FLOW_TOKENS, \
    _EQUALITY_TEST_TOKENS, _LOGIC_TOKENS, _MULTIPLICATION_TOKENS, _UNARY_TOKENS, _IDENTIFIER_TYPES, Token, \
    _ASSIGNMENT_TOKENS
from lexer import Lexer
from tree import UnaryOp, BinOp, FnCall, PropRef, PropCall, Command, Index, Ident
from literals import Duration, Float, Int, Percent, Str, Time, Bool, List, Set
from treedump import DumpTree

EMPTY_SET = Set(Token(tid=TK.EMPTY, tcl=TCL.LITERAL, lex="{}", val=None))


@dataclass
class ParseTree(object):
    def __init__(self, nodes=None, keywords=None, source=None):
        self.nodes = nodes if nodes is not None else []
        self.keywords = keywords if keywords is not None else Scope()
        self.globals = Scope(keywords)
        self.source = source
        load_keywords(self.globals)


class Parser(object):
    def __init__(self, str=None):
        self.keywords = load_keywords(Scope())
        self._lexer = Lexer(string=str, keywords=self.keywords)
        self._skip_end_of_line = True
        self._parse_string = str  # which could be none
        self.nodes = []
        EMPTY_SET.token.value = EMPTY_SET

    # syntactic sugar (use self.peek)
    def __getattr__(self, item):
        if item == 'token':
            return self._lexer.token
        pass

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def peek(self):
        if self.token is None:
            self._lexer.advance()
        return self.token

    # returns current token and advances
    def advance(self, skip_end_of_line=None):
        skip_end_of_line = self._skip_end_of_line if skip_end_of_line is None else skip_end_of_line
        return self._lexer.advance(skip_end_of_line)

    # if current token matches
    def check(self, ex_tid):
        return False if self.token.id == TK.EOF else self.token.id == ex_tid

    # skip over the expected current token.
    def consume(self, ex_tid):
        while self._skip_end_of_line and self.token.id == TK.EOL:
            self.advance(skip_end_of_line=self._skip_end_of_line)
        if self.token.id == ex_tid:
            return self.advance(self._skip_end_of_line)
        _expected(expected=f'{ex_tid.name}', found=self.token)

    def consume_next(self, ex_tid=None):
        token = self.advance()
        if self.token.id == ex_tid:
            return token
        _expected(expected=f'{ex_tid.name}', found=self.token)

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
            if type(node).__name__ != "list":
                self.nodes.append(node)
            else:
                self.nodes += node  # a list can be returned
        tree = ParseTree(nodes=self.nodes, keywords=self.keywords, source=self._parse_string)
        return tree

    # -----------------------------------
    # control language parsing at top
    # -----------------------------------
    def parse_command(self):
        nodes = []
        tk = self.peek()
        if not self.match([TK.EOL]) and tk.id == TK.PCT2:
            self._skip_end_of_line = False
            self.advance()
            while tk.id != TK.EOL:
                tk = Token(tid=TK.COMMAND, tcl=TCL.COMMAND, lex="%%", loc=self._lexer.tell())
                command = Command(tk, self.expression())
                nodes.append(command)
                tk = self.peek()
                if tk.id in [TK.EOF, TK.EOL]:
                    break
            self._skip_end_of_line = True
            return nodes
        self._skip_end_of_line = True
        return self.flow()

    # -----------------------------------
    # Recursive Descent Parser States
    # -----------------------------------
    def expression(self):
        op = self.peek()
        if self.match([TK.DEFINE]):
            node = UnaryOp(op, self.flow())
            self.advance()
        else:
            node = self.parse_command()
            op = self.peek()
            if op.id == TK.SEMI:
                self.advance()
        return node

    def flow(self):
        node = self.set_parameters()
        op = copy(self.token)  # need a copy or we modify the _lexer's token with op.map()
        while op.id in _FLOW_TOKENS:
            sep = op.id
            seq = List(op.map2binop(), [node])
            while self.match([sep]):
                node = self.set_parameters()
                seq.append(node)
            node = seq
            op = copy(self.token)
        return node

    def set_parameters(self):
        node = self.assignment()
        op = self.token
        if op.id == TK.COLN:
            while self.match([TK.COLN]):
                node = BinOp(node, op.map2binop(), self.assignment())
                op = self.token
        return node

    def assignment(self):
        node = self.logic_expr()
        op = self.token
        while self.match(_ASSIGNMENT_TOKENS):
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
            node2 = self.unary()
            # fixup for lack of 2-state lookahead: 1..2 scans as ['1.', '.', '2'] but scanner can only backup 1 token.
            if node is not None and op.id == TK.DOT and node.token.id == TK.FLOT:
                op.id = TK.DOT2
            node = BinOp(node, op.map2binop(), node2)
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
        if token.id == TK.EOL:
            return node
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
        elif token.id == TK.EMPTY:
            node = EMPTY_SET
        elif token.id == TK.LBRC:
            self.consume(TK.LBRC)
            node = Set(token, self.sequence(TK.COMA))
            self.consume(TK.RBRC)
            return node
        elif token.id == TK.LPRN:   # should probably be sequence / tuple literal and parse plists via 'identifier'
            self.advance()
            node = self.expression()
            if self.match([TK.COMA]):
                node = self.plist(node)
            else:
                self.consume(TK.RPRN)
            return node
        elif token.id == TK.LBRK:   # should be list literal and parse indexing via 'identifier'
            self.consume(TK.LBRK)
            node = List(token.map2litval(), self.sequence(TK.COMA))
            self.consume(TK.RBRK)
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
        tk = self.peek()
        token = self.advance()
        if token.id == TK.DOT:
            token = self.consume_next(TK.IDNT)
            node = PropRef(tk, self.identifier())
            if token.id == TK.LPRN:
                node = PropCall(tk, node.member, self.plist())
        elif token.id == TK.DOT2:
            self.advance()
            node = BinOp(left=Ident(tk), op=token.map2binop(), right=self.expression())
        elif token.id == TK.LPRN:
            node = FnCall(tk, self.plist())
        elif token.id == TK.LBRK:
            node = Index(tk, self.idx_list())
        else:
            node = Ident(tk)
        return node

    def idx_list(self, node=None):
        """( EXPR ',' ... )"""
        seq = [] if node is None else [node]
        self.match([TK.LBRK])
        token = copy(self.peek())
        if token.id != TK.RBRK:
            seq = self.sequence(TK.COMA, node)
        self.consume(TK.RBRK)
        token.t_class = TCL.LIST
        token.id = TK.INDEX
        token.lexeme = '['  # fixup token.
        return List(token, seq)

    def plist(self, node=None):
        """( EXPR ',' ... )"""
        seq = [] if node is None else [node]
        self.match([TK.LPRN])
        token = copy(self.peek())
        if token.id != TK.RBRK:
            seq = self.sequence(TK.COMA, node)
        self.consume(TK.RPRN)
        token.t_class = TCL.LIST
        token.id = TK.PARAMETER_LIST
        token.lexeme = '('  # fixup token.
        return List(token, seq)

    def sequence(self, sep, node=None):
        """EXPR <sep> EXPR <sep> ..."""
        seq = [] if node is None else [node]
        while True:
            node = self.expression()
            seq.append(node)
            if self.peek().id != sep:
                break
            self.consume(sep)
        return seq

    def print_symbol_table(self):
        self._symbol_table.print()

    @staticmethod
    def print_tree(node):
        dt = DumpTree()
        viz = dt.apply(node)
        for v in viz:
            print(v)
