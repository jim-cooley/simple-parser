from copy import copy
from dataclasses import dataclass

from exceptions import _expected
from environment import Environment
from tokens import TK, TCL, _ADDITION_TOKENS, _COMPARISON_TOKENS, _FLOW_TOKENS, \
    _EQUALITY_TEST_TOKENS, _LOGIC_TOKENS, _MULTIPLICATION_TOKENS, _UNARY_TOKENS, _IDENTIFIER_TYPES, Token, \
    _ASSIGNMENT_TOKENS
from tokenstream import TokenStream
from tree import UnaryOp, BinOp, FnCall, PropRef, PropCall, Command, Index, Ident, Literal
from literals import Duration, Float, Int, Percent, Str, Time, Bool, List, Set
from treedump import DumpTree

LIT_EMPTY_SET = Set(Token(tid=TK.EMPTY, tcl=TCL.LITERAL, lex="{}", val=None))
LIT_NONE = Literal(Token(tid=TK.NONE, tcl=TCL.LITERAL, lex="none", val=None))


@dataclass
class ParseTree(object):
    def __init__(self, root, values=None, start=None, length=None):
        self.root = root
        self.values = values
        self.tk_start = start
        self.tk_len = length


class Parser(object):
    def __init__(self, environment, verbose=True):
        self.environment = environment
        self.verbose = verbose
        self._skip_end_of_line = True

    # syntactic sugar (use self.peek)
    def __getattr__(self, item):
        if item == 'token':
            return self._peek()
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return self._advance(skip_end_of_line=False)

    # -----------------------------------
    # Parser entry point
    # -----------------------------------
    def parse(self, text):
        self._init(text)
        while True:
            node = self.parse_command()
            if node is None or node.token.id == TK.EOF:
                break
            nodes = [node] if type(node).__name__ != "list" else node
            self.environment.trees += [ParseTree(_) for _ in nodes]
        return self.environment

    def _init(self, text):
        self._tk_stream = TokenStream(source=text)
        self.environment.source = text
        self.environment.lines = text.splitlines()
        self.environment.tokens = self._tk_stream
        self._skip_end_of_line = True

    # -----------------------------------
    # control language parsing at top
    # -----------------------------------
    def parse_command(self):
        commands = []
        tk = self._peek()
        if not self._match([TK.EOL]) and tk.id == TK.PCT2:
            self._skip_end_of_line = False
            self._advance()
            while tk.id != TK.EOL:
                command = Command(tk, self.expression())
                commands.append(command)
                tk = self._peek()
                if tk.id in [TK.EOF, TK.EOL]:
                    break
            self._skip_end_of_line = True
            self.environment.commands += commands
            return None  # commands
        self._skip_end_of_line = True
        return self.expression()

    # -----------------------------------
    # Recursive Descent Parser States
    # -----------------------------------
    def expression(self):
        node = self.parse_definition()
        op = self._peek()
        if op.id == TK.SEMI:
            self._advance()
        return node

    def parse_definition(self):
        op = self._peek()
        if self._match([TK.DEFATTR]):
            node = UnaryOp(op, self.flow())
            return node
        elif op.id == TK.VAR:
            self._advance()
            node = UnaryOp(op, self.assignment())
            return node
        return self.flow()

    def flow(self):
        node = self.set_parameters()
        op = copy(self._peek())  # need a copy or we modify the _lexer's token with op.map()
        while op.id in _FLOW_TOKENS:
            sep = op.id
            seq = List(op.map2binop(), [node])
            while self._match([sep]):
                node = self.set_parameters()
                seq.append(node)
            node = seq
            op = copy(self._peek())
        return node

    def set_parameters(self):
        node = self.assignment()
        op = self._peek()
        if op.id == TK.COLN:
            while self._match([TK.COLN]):
                node = BinOp(node, op.map2binop(), self.assignment())
                op = self._peek()
        return node

    def assignment(self):
        node = self.logic_expr()
        op = self._peek()
        while self._match(_ASSIGNMENT_TOKENS):
            tk = node.token
            if tk.id == TK.PARAMETER_LIST:  # convert to tuple assignment
                TK.id = TK.TUPLE
            elif node.token.t_class not in _IDENTIFIER_TYPES:
                _expected(expected='IDENTIFIER', found=node.token)
            node = BinOp(left=node, op=op.map2binop(), right=self.assignment())
        return node

    def logic_expr(self):
        node = self.equality()
        op = self._peek()
        while self._match(_LOGIC_TOKENS):
            node = BinOp(node, op.map2binop(), self.equality())
            op = self._peek()
        return node

    def equality(self):
        node = self.comparison()
        op = self._peek()
        while self._match(_EQUALITY_TEST_TOKENS):
            node = BinOp(node, op.map2binop(), self.comparison())
            op = self._peek()
        return node

    def comparison(self):
        node = self.term()
        op = self._peek()
        while self._match(_COMPARISON_TOKENS):
            node = BinOp(node, op.map2binop(), self.term())
            op = self._peek()
        return node

    def term(self):
        node = self.factor()
        op = self._peek()
        while self._match(_ADDITION_TOKENS):
            node = BinOp(node, op.map2binop(), self.factor())
            op = self._peek()
        return node

    def factor(self):
        node = self.unary()
        op = self._peek()
        while self._match(_MULTIPLICATION_TOKENS):
            node2 = self.unary()
            # fixup for lack of 2-state lookahead: 1..2 scans as ['1.', '.', '2'] but scanner can only backup 1 token.
            if node is not None and op.id == TK.DOT and node.token.id == TK.FLOT:
                op.id = TK.DOT2
            node = BinOp(node, op.map2binop(), node2)
            op = self._peek()
        return node

    def unary(self):
        op = self._peek()
        if self._match(_UNARY_TOKENS):
            return UnaryOp(op.map2unop(), self.unary())
        node = self.prime()
        if node is not None and node.token.id in [TK.ANY, TK.ALL, TK.NONEOF]:
            node = UnaryOp(node.token, self.unary())
        return node

    def prime(self):
        node = None
        token = self._peek()
        if token.id == TK.EOL:
            return node
        if token.id == TK.FALSE:
            node = Bool(token, False)
        elif token.id == TK.TRUE:
            node = Bool(token, True)
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
            node = LIT_EMPTY_SET
            node.token.location = token.location
        elif token.id == TK.NONE:
            node = Literal(token)
            token.t_class = TCL.LITERAL
        elif token.id == TK.LBRC:
            self._advance()
            node = Set(token, self.sequence(TK.COMA))
            self._consume(TK.RBRC)
            return node
        elif token.id == TK.LPRN:  # should probably be sequence / tuple literal and parse plists via 'identifier'
            self._advance()
            node = self.expression()
            if self._match([TK.COMA]):
                node = self.plist(node)
            else:
                self._consume(TK.RPRN)
            return node
        elif token.id == TK.LBRK:  # should be list literal and parse indexing via 'identifier'
            self._consume(TK.LBRK)
            node = List(token.map2litval(), self.sequence(TK.COMA))
            self._consume(TK.RBRK)
            return node
        elif token.t_class in _IDENTIFIER_TYPES or token.id == TK.IDNT:
            return self.identifier()
        else:
            return node
        self._advance()
        return node

    # -----------------------------------
    # Helpers
    # -----------------------------------
    def identifier(self):
        """
        identifier | identifier ( plist ) | identifier . identifier
        """
        tk = self._advance()
        token = self._peek()
        if token.id == TK.DOT:
            token = self._consume_next(TK.IDNT)
            node = PropRef(tk, self.identifier())
            if token.id == TK.LPRN:
                node = PropCall(tk, node.member, self.plist())
        elif token.id == TK.DOT2:
            self._advance()
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
        self._match([TK.LBRK])
        token = copy(self._peek())
        if token.id != TK.RBRK:
            seq = self.sequence(TK.COMA, node)
        self._consume(TK.RBRK)
        token.t_class = TCL.LIST
        token.id = TK.TUPLE
        token.lexeme = '['  # fixup token.
        return List(token, seq)

    def plist(self, node=None):
        """( EXPR ',' ... )"""
        seq = [] if node is None else [node]
        self._match([TK.LPRN])
        token = copy(self._peek())
        if token.id != TK.RPRN:
            seq = self.sequence(TK.COMA, node)
        self._consume(TK.RPRN)
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
            if self._peek().id != sep:
                break
            self._consume(sep)
        return seq

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def _peek(self):
        return self._tk_stream.peek()

    # returns current token and advances
    def _advance(self):
        while True:
            tk = self._tk_stream.read1()
            if self._skip_end_of_line and tk.id == TK.EOL:
                continue
            break
        return tk

    # if current token matches
    def _check(self, ex_tid):
        tkid = self._peek().id
        return False if tkid == TK.EOF else tkid == ex_tid

    # skip over the expected current token.
    def _consume(self, ex_tid):
        while True:
            tk = self._peek()
            if self._skip_end_of_line and tk.id == TK.EOL:
                self._advance()
                continue
            break
        if self._peek().id == ex_tid:
            return self._advance()
        _expected(expected=f'{ex_tid.name}', found=self._peek())

    def _consume_next(self, ex_tid=None):
        self._advance()
        tk = self._peek()
        if tk.id == ex_tid:
            return tk
        _expected(expected=f'{ex_tid.name}', found=self._peek())

    # match if current token is any of the set.  advance if so.
    def _match(self, tk_list):
        tk = self._peek()
        if tk is None or tk.id == TK.EOF:
            return False
        if tk.id in tk_list:
            self._advance()
            return True
        return False

    def print_symbol_table(self):
        self._symbol_table.printall()

    @staticmethod
    def print_tree(node):
        dt = DumpTree()
        viz = dt.apply(node)
        for v in viz:
            print(v)
