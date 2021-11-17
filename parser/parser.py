from copy import copy
from dataclasses import dataclass

from runtime.environment import Environment
from runtime.exceptions import FocalError, getLogFacility
from runtime.options import getOptions
from runtime.token_data import ADDITION_TOKENS, COMPARISON_TOKENS, FLOW_TOKENS, \
    EQUALITY_TEST_TOKENS, LOGIC_TOKENS, MULTIPLICATION_TOKENS, UNARY_TOKENS, IDENTIFIER_TYPES, ASSIGNMENT_TOKENS, \
    SET_UNARY_TOKENS, IDENTIFIER_TOKENS, IDENTIFIER_TOKENS_EX, ASSIGNMENT_TOKENS_REF, \
    VALUE_TOKENS
from runtime.token_class import TCL
from runtime.token import Token
from runtime.token_ids import TK
from runtime.tree import UnaryOp, BinOp, Command, Assign, Get, FnCall, Index, PropRef, Define, DefineFn, DefineVar, \
    DefineVarFn, ApplyChainProd, Ref, FnRef, Return, IfThenElse, Generate
from runtime.scope import Block, Flow, Function
from runtime.literals import Duration, Float, Int, Percent, Str, Time, Bool, List, Set, Literal

from parser.rewrites import RewriteGets2Refs, RewriteFnCall2DefineFn, RewriteFnCall2FnDef
from parser.lexer import Lexer


@dataclass
class ParseTree(object):
    def __init__(self, root, values=None, start=None, length=None):
        self.root = root
        self.values = values if values is not None else [root.value]
        # UNODNE: place source, tokens, lines here?  Except original source is shared amongst trees in a forest


class Parser(object):
    def __init__(self):
        self.environment = None
        self.logger = getLogFacility('focal')
        self.options = getOptions('focal')
        self._skip_end_of_line = True

    @property
    def token(self):
        return self.peek()

    def __iter__(self):
        return self

    def __next__(self):
        return self.advance()

    # -----------------------------------
    # Parser entry point
    # -----------------------------------
    def parse(self, environment=None, source=None):
        environment = self._init(environment, source)
        self.environment = environment
        while True:
            if not self._lexer.seek(0, Lexer.SEEK.NEXT):
                break
            decl = self.declaration()
            tkid = self.peek().id
            if decl is not None:
                decls = [decl] if type(decl).__name__ != "list" else decl
                environment.trees += [ParseTree(_) for _ in decls]
            elif tkid != TK.EOF:  # decl is None
                continue
            elif tkid == TK.EOF or decl.token.id == TK.EOF:
                break
        return environment

    def _init(self, environment=None, source=None):
        self._lexer = Lexer(source=source)
        logger = getLogFacility('focal')
        if environment is None:
            environment = Environment()
        environment.commands = []
        environment.trees = []
        environment.source = source
        environment.lines = source.splitlines()
        environment.tokens = self._lexer
        Environment.current = environment
        logger.lines = environment.lines
        self._skip_end_of_line = True
        return environment

    # UNDONE: removing commands from this parse will simplify MANY things
    def command(self):
        tk = self.peek()
        commands = []
        self._skip_end_of_line = False
        self.advance()
        while tk.id != TK.EOL:
            command = Command(tk, self.expression())
            if command is None:
                self.logger.error(self.peek(), "Invalid token")
                break
            commands.append(command)
            tk = self.peek()
            if tk.id in [TK.EOF, TK.EOL]:
                break
            tk = self.consume(TK.SEMI, expect=False)  # optional semi-colon
        self._skip_end_of_line = True
        self.environment.commands += commands
        return

    # -----------------------------------
    # Recursive Descent Parser Entry
    # -----------------------------------
    def declaration(self):
        try:
            if self.match1(TK.PCT2):
                self.command()
                return None
            elif self.match1(TK.VAR):
                return self.var()
            elif self.match1(TK.DEFINE):
                return self.definition()
            return self.statement()
        except FocalError as se:
            self.synchronize()
            raise se
        except Exception as e:
            self.logger.report(e, loc=self.peek().location)
            if self.options.throw_errors:
                raise e

    def statement(self):
        op = self.peek()
        if self.match1(TK.IF):
            test = self.block_expr()
            self.consume(TK.THEN)
            thn = self.block_expr()
            els = None
            if self.match1(TK.ELSE):
                els = self.block_expr()
            node = IfThenElse(test=test, then=thn, els=els)
        else:
            node = self.block_expr()
            if node is None:
                self.logger.warning(f'Unexpected token: {self.peek()}', self.peek().location)
                self.advance()  # attempt to recover
                node = self.block_expr()
            if self.peek().id == TK.EOF:
                return node
            if self.match([TK.SEMI, TK.COMA]):
                return node
        return node

    # -----------------------------------
    # Error Recovery
    # -----------------------------------
    def synchronize(self):
        while True:
            self.advance()
            if self.peek(-1).id in [TK.SEMI, TK.EOF, TK.EOL]:  # just passed
                return
            tkid = self.peek().id  # just landed on
            if tkid in [TK.BLOCK, TK.DEF, TK.DEFINE, TK.COMMAND, TK.VAR, TK.FUNCTION, TK.EOF]:
                return

    # -----------------------------------
    # 'statement' parsing at top
    # -----------------------------------
    def block_expr(self):
        tk = self.peek()
        if tk.id == TK.LBRC:
            node = self.expression()    # UNDONE: self.definition(), or just parse the block() ?
            if self.match1(TK.COLN):
                op = self.peek(-1)
                tid = self.peek().id
                if tid == TK.LBRC:
                    node = BinOp(left=node, op=op.set_id(TK.APPLY), right=self.statement())
                elif tid == TK.LPRN:
                    node = BinOp(left=node, op=op.set_id(TK.APPLY), right=self.tuple())
                else:
                    self.logger.error("Expected '{' or '(' after ':')"
                                      f'{self.peek()}', self.peek().location)
            if self.peek().id in FLOW_TOKENS:
                return self.parse_flow(node)
            else:
                return node
        elif self.check(SET_UNARY_TOKENS):
            if self.peek(1).id != TK.COLN:
                return self.expression()
            self.consume(tk.id)
            self.consume(TK.COLN)
            if self.peek().id != TK.LBRC:
                self.logger.expected(expected=f'TK.LRBC', found=self.peek())
            return UnaryOp(tk, self.block_expr())
        else:
            return self.expression()

    def definition(self):
        l_expr = self.statement()  # l-value cannot include flows
        if isinstance(l_expr, Define):
            op = l_expr.token
        else:
            op = self.advance()
        if _is_valid_l_value(l_expr):
            l_expr = _rewriteFnCall2Definition(l_expr)
            if isinstance(l_expr, DefineFn) or isinstance(l_expr, DefineVarFn):
                return l_expr
            elif isinstance(l_expr, FnCall):  # keyword overrides other syntax
                return DefineFn(left=l_expr.left, op=op, right=self.block_expr2(), args=l_expr.right)
            else:
                return Define(left=l_expr.left, op=op, right=l_expr.right)
        self.logger.error(f"Invalid assignment target {l_expr}", op.location)
        return l_expr

    def var(self):
        l_expr = self.statement()  # l-value cannot include flows
        if isinstance(l_expr, Define):
            op = l_expr.token
        else:
            op = self.advance()
        if _is_valid_l_value(l_expr):
            l_expr = _rewriteFnCall2Definition(l_expr)
            if isinstance(l_expr, DefineVar):
                return l_expr
            elif isinstance(l_expr, FnCall):
                return DefineVarFn(left=l_expr.left, op=op, right=self.block_expr2(), args=l_expr.right)
            elif isinstance(l_expr, DefineFn):
                return DefineVarFn(left=l_expr.left, op=op, right=l_expr.right, args=l_expr.args)
            else:
                return DefineVar(l_expr.left, op, l_expr.right)
        self.logger.error("Invalid assignment target", op.location)
        return l_expr

    # -----------------------------------
    # Expression Entry
    # -----------------------------------
    def expression(self):
        return self.flow()

    def flow(self):
        op = self.peek()
        if self.match1(TK.RETURN):
            node = Return(token=op, expr=self.block_expr())
        else:
            node = self.tuple()
            if node is None:
                return None
            if self.peek().id in FLOW_TOKENS:
                return self.parse_flow(node)
        return node

    def parse_flow(self, node=None):
        op = copy(self.peek())
        while op.id in FLOW_TOKENS:
            sep = op.id
            seq = Flow(op.remap2binop(), [node] if node is not None else [])
            while self.match1(sep):
                node = self.assignment()
                if node is not None:
                    if len(seq) > 0:
                        node = _rewriteGets(node)
                    seq.append(node)
                else:
                    break
            node = seq
            last = seq.last
            if isinstance(last, Get):
                last = last.to_ref()
            if isinstance(last, Ref):
                if op.id in [TK.RARR, TK.RAISE]:
                    seq.last = ApplyChainProd(left=last, tid=TK.RAISE, lex=seq.token.lexeme, loc=last.token.location)
                else:
                    seq.last = ApplyChainProd(left=last, lex=seq.token.lexeme, loc=last.token.location)
            op = copy(self.peek())
        return node

    def tuple(self):
        l_expr = self.assignment()
        op = self.peek()
        if op.id == TK.COLN:
            tid = l_expr.token.id
            if tid in SET_UNARY_TOKENS:
                op.id = tid
                op.lexeme = l_expr.token.lexeme + ':'
                self.advance()
                l_expr = UnaryOp(op.remap2unop(), self.tuple())
                return l_expr
            while self.match1(TK.COLN):
                l_expr = _rewriteGets(l_expr)
                if l_expr.token.id == TK.FUNCTION:
                    l_expr = DefineFn(left=l_expr.left, op=op, args=l_expr.right, right=self.tuple())
                else:
                    l_expr = Define(left=l_expr, op=op, right=self.tuple())
                op = self.peek()
        return l_expr

    def assignment(self):
        l_expr = self.boolean_expr()  # l-value cannot include flows
        if l_expr is None:
            return None
        op = self.peek()
        if op.id in [TK.GTR2, TK.APPLY]:
            return l_expr
        elif self.match(ASSIGNMENT_TOKENS):
            if l_expr.token.id in IDENTIFIER_TOKENS_EX:
                if hasattr(l_expr, 'left'):
                    if l_expr.left.token.is_reserved:
                        self.logger.error(f'Invalid assignment target: {l_expr.left.token.lexeme} is reserved',
                                          op.location)
                if l_expr.is_lvalue:
                    r_expr = self.block_expr()
                    return self.process_assignment(op=op, l_expr=l_expr, r_expr=r_expr)

                if isinstance(l_expr, BinOp):
                    self.logger.error(f'Invalid assignment target: {l_expr.left.token.lexeme}', op.location)
            self.logger.error(f'Invalid assignment target: {l_expr.token}', op.location)
        elif self.match1(TK.EQGT):
            if l_expr.token.id not in IDENTIFIER_TOKENS_EX:
                self.logger.error(f'Invalid assignment target: {l_expr.token}', op.location)
            r_expr = self.block_expr2()
            l_expr = _rewriteFnCall2FnDef(l_expr)
            if isinstance(l_expr, FnCall):
                return DefineFn(left=l_expr.left, op=op, right=r_expr, args=l_expr.right)
            elif isinstance(l_expr, FnRef):
                return DefineFn(left=l_expr.left, op=op, right=r_expr, args=l_expr.right)
            elif isinstance(l_expr, Ref):
                if isinstance(r_expr, Define):
                    return DefineFn(left=l_expr, op=op, right=r_expr.right,
                                    args=List([r_expr.left], Token.TUPLE(loc=r_expr.token.location)))
            return DefineFn(left=l_expr, op=op, right=r_expr, args=None)  # parameterless function
        return l_expr

    def block_expr2(self):  # new block expression parsing for =>
        tk = self.peek()
        if self.match1(TK.LBRC):
            node = self.block(is_lvalue=False)
            self.consume(TK.RBRC)
            if self.match1(TK.COLN):
                op = self.peek(-1)
                tid = self.peek().id
                if tid == TK.LBRC:
                    node = BinOp(left=node, op=op.set_id(TK.APPLY), right=self.statement())
                elif tid == TK.LPRN:
                    node = BinOp(left=node, op=op.set_id(TK.APPLY), right=self.tuple())
                else:
                    self.logger.error("Expected '{' or '(' after ':')"
                                      f'{self.peek()}', self.peek().location)
            return node
        return self.expression()

    def process_assignment(self, op, l_expr, r_expr):
        if l_expr.token.id in IDENTIFIER_TOKENS_EX or l_expr.token.t_class is TCL.IDENTIFIER:
            if op.id in ASSIGNMENT_TOKENS_REF:
                l_expr = _rewriteFnCall2Definition(l_expr)
            if op.id in [TK.EQLS, TK.EQGT]:
                if isinstance(l_expr, FnCall) or isinstance(l_expr, FnRef) or isinstance(l_expr, DefineFn):
                    return DefineFn(left=l_expr.left, op=op, right=r_expr, args=l_expr.right)
                else:
                    return Define(left=l_expr, op=op, right=r_expr)
            elif op.id == TK.COEQ:
                if isinstance(l_expr, FnCall) or isinstance(l_expr, FnRef):
                    return DefineVarFn(left=l_expr.left, op=op, right=r_expr, args=l_expr.right)
                else:
                    return DefineVar(left=l_expr, op=op, right=r_expr)
            else:
                return Assign(l_expr, op, r_expr)
        token = l_expr.token if not hasattr(l_expr, 'left') else l_expr.left.token
        self.logger.error(f'Invalid assignment target: {token}', op.location)

    def boolean_expr(self):
        node = self.equality()
        op = self.peek()
        while self.match(LOGIC_TOKENS):
            node = BinOp(left=node, op=op.remap2binop(), right=self.equality())
            op = self.peek()
        return node

    def equality(self):
        node = self.comparison()
        op = self.peek()
        while self.match(EQUALITY_TEST_TOKENS):
            node = BinOp(left=node, op=op.remap2binop(), right=self.comparison())
            op = self.peek()
        return node

    def comparison(self):
        node = self.term()
        op = self.peek()
        while self.match(COMPARISON_TOKENS):
            node = BinOp(left=node, op=op.remap2binop(), right=self.term())
            op = self.peek()
        return node

    def term(self):
        node = self.factor()
        op = self.peek()
        while self.match(ADDITION_TOKENS):
            node = BinOp(left=node, op=op.remap2binop(), right=self.factor())
            op = self.peek()
        return node

    def factor(self):
        l_node = self.unary()
        op = self.peek()
        while self.match(MULTIPLICATION_TOKENS):
            r_node = self.unary()
            # fixup for lack of 2-state lookahead: 1..2 scans as ['1.', '.', '2'] but scanner can only backup 1 token.
            if op.id == TK.DOT:
                if l_node is not None:
                    if l_node.token.id == TK.FLOT:
                        op.id = TK.DOT2
                elif r_node.token.id == TK.INT:  # l_node is None
                    s_val = f'.{r_node.value}'
                    r_node.token.id = TK.FLOT
                    r_node.token.lexeme = s_val
                    r_node.value = float(s_val)
                    l_node = Float(token=r_node.token)
                    return l_node
            if l_node is None:
                self.logger.error("Invalid assignment target", op.location)
            l_node = BinOp(left=l_node, op=op.remap2binop(), right=r_node)
            op = self.peek()
        return l_node

    def unary(self):
        op = self.peek()
        if self.match(UNARY_TOKENS):
            node = UnaryOp(op.remap2unop(), self.unary())
            return node
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
            node = Literal.FALSE(loc=token.location)
        elif token.id == TK.TRUE:
            node = Literal.TRUE(loc=token.location)
        elif token.id == TK.INT:
            node = Int(token=token)
        elif token.id == TK.FLOT:
            node = Float(token=token)
        elif token.id == TK.PCT:
            node = Percent(token=token)
        elif token.id == TK.DUR:
            node = Duration(token=token)
        elif token.id == TK.TIME:
            node = Time(token=token)
        elif token.id == TK.QUOT:
            node = Str(token=token)
        elif token.id == TK.EMPTY:
            node = Literal.EMPTY(loc=token.location)
        elif token.id == TK.NONE:
            node = Literal.NONE(loc=token.location)
        elif token.id == TK.LBRC:
            self.advance()
            node = self.block()
#           node = Set(token, self.sequence())
            self.consume(TK.RBRC)
            return node
        elif token.id == TK.LPRN:
            self.advance()
            node = self.expression()
            if self.check1(TK.COMA):
                node = self.plist(node)
            else:
                self.consume(TK.RPRN)
            return node
        elif token.id == TK.LBRK:
            self.consume(TK.LBRK)
            node = self.series()
            self.consume(TK.RBRK)
            return node
        elif token.t_class in IDENTIFIER_TYPES or token.id in [TK.IDENT, TK.ANON]:
            return self.identifier()
        else:
            return node
        self.advance()
        return node

    # -----------------------------------
    # leaf state helpers
    # -----------------------------------
    def block(self, is_lvalue=True):
        seq = []
        tk = self.peek()
        loc = tk.location
        is_lvalue_strict = is_lvalue    # no assignment or operators on rhs of included exprs

        while self.peek().id != TK.EOF and self.peek().id != TK.RBRC:
            decl = self.declaration()
            seq.append(decl)
            #            if self.peek().id == TK.RBRC:   # must check closure before (empty set) and after as decl can finish parsing
            #                break
            if is_lvalue:
                if hasattr(decl, 'is_lvalue'):
                    is_lvalue = decl.is_lvalue
                elif not isinstance(decl, Literal) and not isinstance(decl, Get):
                    if decl.token.id not in [TK.COLN, TK.EQLS]:
                        is_lvalue_strict = is_lvalue = False
                if is_lvalue_strict:
                    if decl.token.id not in VALUE_TOKENS:
                        if decl.token.id not in [TK.COLN]:
                            is_lvalue_strict = False
                            if hasattr(decl, 'right'):
                                if decl.right is not None:
                                    if decl.right.token.id in VALUE_TOKENS:
                                        is_lvalue_strict = True
                                else:
                                    is_lvalue_strict = False
        if len(seq) == 0:
            return Set(seq, Token.EMPTY(loc=loc))
        elif is_lvalue and is_lvalue_strict:
            return Set(seq, Token.SET(loc=loc))
        else:
            return Block(items=seq, loc=loc)

    def identifier(self):
        """
        identifier | identifier ( plist ) | identifier . identifier
        """
        tk = self.advance()
        ident = self.environment.keywords.find(token=tk)
        token = self.peek()
        if token.id == TK.DOT:
            token = self.consume_next(TK.IDENT)
            node = PropRef(ref=Get(tk), member=self.identifier())
        elif token.id == TK.DOT2:
            self.advance()
            node = BinOp(left=Ref(tk), op=token.remap2binop(), right=self.expression())
        elif token.id == TK.LPRN:
            plist = self.plist()
            plist.token.id = TK.TUPLE
            node = FnCall(ref=Get(tk), parameters=plist)
        elif token.id == TK.LBRK:
            node = Index(ref=Get(tk), parameters=self.idx_list())
        else:
            if isinstance(ident, Function) or tk.t_class == TCL.FUNCTION:
                node = FnCall(ref=Get(tk), parameters=None)
            else:
                is_lval = self.check(ASSIGNMENT_TOKENS_REF)
                node = Ref(tk) if is_lval else Get(tk)
        return node

    def idx_list(self, node=None):
        """( EXPR ',' ... )"""
        seq = [] if node is None else [node]
        self.match([TK.LBRK])
        token = copy(self.peek())
        if token.id != TK.RBRK:
            seq = self.sequence(node)
        self.consume(TK.RBRK)
        return List(seq, Token.TUPLE(loc=token.location))

    def plist(self, node=None):
        """( EXPR ',' ... )"""
        seq = [] if node is None else [node]
        self.match1(TK.LPRN)
        token = copy(self.peek())
        is_tuple = self.match1(TK.COMA)
        if token.id != TK.RPRN:
            seq = self.sequence(node)
        self.consume(TK.RPRN)
        if is_tuple or len(seq) > 1:
            token = Token.TUPLE(loc=token.location)
            if seq[len(seq) - 1] is None:
                seq.pop()
        else:
            token = Token.LIST(loc=token.location)
        token.lexeme = '('  # fixup token.
        return List(items=seq, token=token)

    def series(self):
        """
        Parse a potential Series() object.  If not determined to be a Series, it is returned as a List.
        The key determinate is that Series() objects are allowed to have labels, which are expressed as k:v pairs.
        Series also parses out optional 'index=' and 'name=' clauses.
        Lists are simple values or identifiers, or possibly identifer / literal expressions but do not have labels.
        :param token: Optional.  Taken as the originating token & mapped to an appropriate Literal for Lists
        :return: Series() or List() object
        """
        seq = []
        is_series = False
        loc = self._lexer.get_location()
        if self.peek().id == TK.RBRK:
            return Literal.EMPTY_LIST(loc=loc)
        while True:
            expr = self.expression()
            if not is_series:
                if expr.token.id in [TK.COLN, TK.DEFINE, TK.EQLS]:
                    is_series = True
            seq.append(expr)
            if not self.match1(TK.COMA):
                break
        node = Generate(target=(TK.SERIES if is_series else TK.LIST), parameters=seq, loc=loc)
        return node

    def sequence(self, node=None):
        """EXPR <sep> EX1PR <sep> ..."""
        seq = [] if node is None else [node]
        while True:
            seq.append(self.expression())
            if not self.match1(TK.COMA):
                break
        return seq

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def peek(self, rel=0):
        tk = self._lexer.peek(rel=rel)
        if not self._skip_end_of_line or tk.id != TK.EOL:
            return tk
        self._lexer.seek(1, Lexer.SEEK.NEXT)
        return self._lexer.peek()

    # returns current token and advances
    def advance(self):
        while True:
            tk = self._lexer.read1()
            if tk.id == TK.EOL:
                if self._skip_end_of_line:
                    continue
            break
        while True:
            if self._skip_end_of_line and self.peek().id == TK.EOL:
                self._lexer.read1()
                continue
            break
        return tk

    # if current token matches
    def check1(self, ex_tid, rel=0):
        tkid = self.peek(rel=rel).id
        return False if tkid == TK.EOF else tkid == ex_tid

    def check(self, tl_list, rel=0):
        return self.peek(rel=rel).id in tl_list

    def check_lvalue(self, l_expr, location=None):
        if hasattr(l_expr, 'left'):
            if l_expr.left.token.is_reserved:
                self.logger.error(f'Invalid assignment target: {l_expr.left.token.lexeme} is reserved',
                                  location)
        return l_expr.is_lvalue

    # skip over the expected current token.
    def consume(self, ex_tid, expect=True):
        while True:
            tk = self.peek()
            if self._skip_end_of_line and tk.id == TK.EOL:
                self.advance()
                continue
            break
        if self.peek().id == ex_tid:
            self.advance()
            return self.peek()
        if expect:
            self.logger.expected(expected=f'{ex_tid.name}', found=self.peek())

    def consume_next(self, ex_tid=None):
        self.advance()
        tk = self.peek()
        if tk.id == ex_tid:
            return tk
        self.logger.expected(expected=f'{ex_tid.name}', found=self.peek())

    # match if current token is any of the set.  advance if so.
    def match(self, tk_list):
        tk = self.peek()
        if tk is None or tk.id == TK.EOF:
            return False
        if tk.id in tk_list:
            self.advance()
            return True
        return False

    def match1(self, tkid):
        tk = self.peek()
        if tk is None or tk.id == TK.EOF:
            return False
        if tk.id == tkid:
            self.advance()
            return True
        return False

    def print_symbol_table(self):
        self._symbol_table.printall()


def _rewriteGets(node):
    rewriter = RewriteGets2Refs()
    return rewriter.apply(node)


def _rewriteFnCall2Definition(node):
    rewriter = RewriteFnCall2DefineFn()
    rval = rewriter.apply(node)
    return rval


def _rewriteFnCall2FnDef(node):
    rewriter = RewriteFnCall2FnDef()
    rval = rewriter.apply(node)
    return rval


def _is_valid_l_value(l_expr):
    if l_expr.token.id in IDENTIFIER_TOKENS:
        return True
    elif isinstance(l_expr, Define):
        return True
    elif isinstance(l_expr, BinOp):
        return _is_valid_l_value(l_expr.left)
    else:
        return False
