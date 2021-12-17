from copy import copy
from dataclasses import dataclass

from parser.tokenstream import TokenStream
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
from runtime.tree import UnaryOp, BinOp, Assign, Get, FnCall, Index, PropRef, Define, DefineFn, DefineVar, \
    DefineVarFn, ApplyChainProd, Ref, FnRef, Return, IfThenElse, Generate, Combine, GenerateRange, Slice, PropCall, \
    PropSet, IndexSet
from runtime.scope import Block, Flow
from runtime.function import Function
from runtime.literals import Float, Int, Percent, Str, Bool, Literal
from runtime.time import Time, Duration
from runtime.collections import Set, List, Tuple, NamedTuple, build_collection, lit_collection

from parser.rewrites import RewriteGets2Refs, RewriteFnCall2DefineFn, RewriteFnCall2FnDef


@dataclass
class ParseTree(object):
    def __init__(self, root, values=None, start=None, length=None):
        self.root = root
        self.values = values if values is not None else [root.value]


class Parser(object):
    def __init__(self):
        self.environment = None
        self.logger = getLogFacility('focal')
        self.options = getOptions('focal')

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
            tkid = self.peek().id
            if tkid == TK.EOF:
                break
            decl = self.declaration()
            tkid = self.peek().id
            if decl is not None:
                decls = [decl] if type(decl).__name__ != "list" else decl
                environment.trees += [ParseTree(_) for _ in decls]
            elif tkid != TK.EOF:  # decl is None
                continue
            if tkid == TK.EOF or decl.token.id == TK.EOF:
                break
        return environment

    def _init(self, environment=None, source=None):
        self.tokens = TokenStream(source=source)
        if environment is None:
            environment = Environment()
        environment.set(source=source, tokens=self.tokens, current=True)
        return environment

    # -----------------------------------
    # Recursive Descent Parser Entry
    # -----------------------------------
    def declaration(self):
        try:
            if self.match1(TK.VAR):
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
        if self.match1(TK.IF):
            test = self.expression()
            self.consume(TK.THEN)
            thn = self.expression()
            els = None
            if self.match1(TK.ELSE):
                els = self.expression()
            node = IfThenElse(test=test, then=thn, els=els)
        else:
            node = self.expression()
            if node is None:
                self.logger.warning(f'Unexpected token: {self.peek()}', self.peek().location)
                self.advance()  # attempt to recover
                node = self.expression()
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
            if self.peek(-1).id in [TK.SEMI, TK.EOF, TK.RBRC]:  # just passed
                return
            tkid = self.peek().id  # just landed on
            if tkid in [TK.BLOCK, TK.DEF, TK.DEFINE, TK.COMMAND, TK.VAR, TK.FUNCTION, TK.EOF]:
                return

    # -----------------------------------
    # Expression Entry
    # -----------------------------------
    def expression(self):
        return self.flow()

    def flow(self):
        op = self.peek()
        if self.match1(TK.RETURN):
            node = Return(token=op, expr=self.expression())
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
                    l_expr = DefineFn(left=l_expr.left, op=op.remap2binop(), args=l_expr.right, right=self.tuple())
                else:
                    l_expr = Combine(left=l_expr, right=self.tuple(), loc=op.location)
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
                    r_expr = self.expression()
                    return self.process_assignment(op=op, l_expr=l_expr, r_expr=r_expr)
                if isinstance(l_expr, BinOp):
                    self.logger.error(f'Invalid assignment target: {l_expr.left.token.lexeme}', op.location)
            self.logger.error(f'Invalid assignment target: {l_expr.token}', op.location)
        elif self.match1(TK.EQGT):
            if l_expr.token.id not in IDENTIFIER_TOKENS_EX:
                self.logger.error(f'Invalid assignment target: {l_expr.token}', op.location)
            r_expr = self.block_expr()
            l_expr = _rewriteFnCall2FnDef(l_expr)
            if isinstance(l_expr, FnCall):
                return DefineFn(left=l_expr.left, op=op.remap2binop(), right=r_expr, args=l_expr.right)
            elif isinstance(l_expr, FnRef):
                return DefineFn(left=l_expr.left, op=op.remap2binop(), right=r_expr, args=l_expr.right)
            elif isinstance(l_expr, Ref):
                if isinstance(r_expr, Define):
                    return DefineFn(left=l_expr, op=op.remap2binop(), right=r_expr.right,
                                    args=List([r_expr.left], Token.TUPLE(loc=r_expr.token.location)))
            return DefineFn(left=l_expr, op=op.remap2binop(), right=r_expr, args=None)  # parameterless function
        return l_expr

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
            op.remap2binop()
            if op.id == TK.RANGE:
                l_node = GenerateRange(start=l_node, end=r_node, loc=l_node.token.location)
            else:
                l_node = BinOp(left=l_node, op=op, right=r_node)
            op = self.peek()
        return l_node

    def unary(self):
        op = self.peek()
        if self.match(UNARY_TOKENS):
            node = UnaryOp(op.remap2unop(), self.unary())
            return node
        if op.id == TK.NONE:
            if self.peek(1).id == TK.COLN:
                op.set_id(TK.NONEOF)
        if self.match(SET_UNARY_TOKENS):
            self.consume(TK.COLN)
            expr = self.unary()
            if self.match1(TK.COLN):
                expr = Combine(left=expr, right=self.tuple(), loc=op.location)
            node = UnaryOp(op.remap2unop(), expr)
            return node
        node = self.prime()
        return node

    def prime(self):
        node = None
        token = self.peek()
        if token.id == TK.EOL:
            return node
        if token.id == TK.FALSE:
            node = Bool.FALSE(loc=token.location)
        elif token.id == TK.TRUE:
            node = Bool.TRUE(loc=token.location)
        elif token.id == TK.INT:
            node = Int(token=token)
        elif token.id == TK.FLOT:
            node = Float(token=token)
        elif token.id == TK.PCT:
            node = Percent(token=token)
        elif token.id == TK.DUR:
            node = Duration(token=token)
        elif token.id == TK.TIME:
            node = Str(token=token)
        elif token.id == TK.QUOT:
            node = Str(token=token)
        elif token.id == TK.EMPTY:
            node = Literal.EMPTY(loc=token.location)
        elif token.id == TK.NONE:
            node = Literal.NONE(loc=token.location)
        elif token.id == TK.LBRC:
            self.advance()
            node = self.block()
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
                return DefineFn(left=l_expr.left, op=op, right=self.block_expr(), args=l_expr.right)
            else:
                return Define(left=l_expr.left, op=op, right=l_expr.right)  # DEFINE var, def ?
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
                return DefineVarFn(left=l_expr.left, op=op, right=self.block_expr(), args=l_expr.right)
            elif isinstance(l_expr, DefineFn):
                return DefineVarFn(left=l_expr.left, op=op, right=l_expr.right, args=l_expr.args)
            else:
                return DefineVar(l_expr.left, op, l_expr.right)
        self.logger.error("Invalid assignment target", op.location)
        return l_expr

    def process_assignment(self, op, l_expr, r_expr):
        if l_expr.token.id in IDENTIFIER_TOKENS_EX or l_expr.token.t_class is TCL.IDENTIFIER:
            if op.id in ASSIGNMENT_TOKENS_REF:
                l_expr = _rewriteFnCall2Definition(l_expr)
            if op.id == TK.EQLS:
                if isinstance(l_expr, Index):
                    return IndexSet(ref=l_expr.ref, index=l_expr.right, value=r_expr)  # common DEFINE '=' Assignment
                elif isinstance(l_expr, PropCall):
                    return IndexSet(ref=l_expr.ref, index=l_expr.right, member=l_expr.member, value=r_expr)
                elif isinstance(l_expr, FnCall) or isinstance(l_expr, FnRef) or isinstance(l_expr, DefineFn):
                    return DefineFn(left=l_expr.left, op=op.remap2binop(), right=r_expr, args=l_expr.right)
                elif isinstance(l_expr, PropRef):
                    return PropSet(ref=l_expr.left, member=l_expr.right, value=r_expr)
                else:
                    return Define(left=l_expr, op=op.remap2binop(), right=r_expr)  # common DEFINE '=' Assignment
            elif op.id == TK.COEQ:
                if isinstance(l_expr, FnCall) or isinstance(l_expr, FnRef):
                    return DefineVarFn(left=l_expr.left, op=op.remap2binop(), right=r_expr, args=l_expr.right)
                else:
                    return DefineVar(left=l_expr, op=op.remap2binop(), right=r_expr)
            elif op.id == TK.EQGT:
                if isinstance(l_expr, FnCall) or isinstance(l_expr, FnRef) or isinstance(l_expr, DefineFn):
                    return DefineFn(left=l_expr.left, op=op.remap2binop(), right=r_expr, args=l_expr.right)
                else:
                    return Define(left=l_expr, op=op.remap2binop(), right=r_expr)
            else:
                return Assign(l_expr, op.remap2binop(), r_expr)
        token = l_expr.token if not hasattr(l_expr, 'left') else l_expr.left.token
        self.logger.error(f'Invalid assignment target: {token}', op.location)

    def block_expr(self):  # new block expression parsing for =>
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

    def block(self, is_lvalue=True):
        seq = []
        tk = self.peek()
        loc = tk.location
        cid = TK.SET
        while self.peek().id != TK.EOF and self.peek().id != TK.RBRC:
            decl = self.declaration()
            seq.append(decl)
            if isinstance(decl, Combine):
                if cid == TK.SET:
                    cid = TK.DATAFRAME
                if isinstance(decl.right, Assign):  # combine with an assign is an expression
                    cid = TK.BLOCK
            elif isinstance(decl, Assign):
                if cid == TK.SET:
                    cid = TK.BLOCK
            elif type(decl).__name__ in ['IfThenElse', 'Return', 'DefineFn', 'DefineVarFn', 'PropSet', 'Block', 'Flow', 'ApplyChainProd', 'Apply']:
                cid = TK.BLOCK
            if self.peek(-1).id in [TK.COLN]:  # declaration() eats the separator
                cid = TK.DATAFRAME
        if len(seq) == 0:
            return Set(seq, Token.EMPTY(loc=loc))
        elif cid != TK.BLOCK:
            return build_collection(cid, items=seq, loc=loc)
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
            prop = self.identifier()
            if isinstance(prop, FnCall):
                node = PropCall(ref=Get(tk), member=prop.left, parameters=prop.paramters)
            else:
                node = PropRef(ref=Get(tk), member=prop)
        elif token.id == TK.DOT2:
            self.advance()
            node = BinOp(left=Ref(tk), op=token.remap2binop(), right=self.expression())
        elif token.id == TK.LPRN:
            plist = self.plist()
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

    def idx_list(self):
        """( EXPR ',' ... )"""
        self.match([TK.LBRK])
        token = self.peek()
        seq = None
        if token.id != TK.RBRK:
            seq = self.idx_slice()
        self.consume(TK.RBRK)
        if seq is None:
            return List(None, Token.TUPLE(loc=token.location))
        else:
            return seq

    def idx_slice(self, node=None):
        """( from ':' to '::' step | term [, term] )"""
        seq = []
        start = end = step = None
        tid = TK.INDEX
        while True:
            token = self.peek()
            if token.id == TK.RBRK:
                break
            if token.id in [TK.COLN, TK.COMN]:
                tid = TK.SLICE
                self.advance()
                u = self.unary()
                if u is not None:
                    if token.id == TK.COMN:
                        u = UnaryOp(Token.NEG(loc=token.location), end)
                    if end is not None:
                        step = u
                    else:
                        end = u
            elif token.id == TK.CLN2:
                tid = TK.SLICE
                self.advance()
                step = self.unary()
            else:
                start = self.boolean_expr()
                if start is not None:
                    seq.append(start)
                token = self.peek()
                if token.id not in [TK.COMA, TK.COLN, TK.COMN, TK.CLN2]:
                    break
                if token.id == TK.COMA:
                    self.advance()
        if tid == TK.INDEX:
            return List(seq, Token.TUPLE(loc=token.location))
        else:
            if len(seq) == 0:
                seq = [start, end, step]
            if len(seq) == 1:
                seq.append(end)
            if len(seq) == 2:
                seq.append(step)
            return Slice(start=seq[0], end=seq[1], step=seq[2], loc=token.location)

    def plist(self, node=None):
        """( EXPR ',' ... )"""
        cid = TK.LIST
        is_literal = True
        seq = [] if node is None else [node]
        self.match1(TK.LPRN)
        token = copy(self.peek())
        if self.match1(TK.COMA):
            cid = TK.TUPLE
        if token.id != TK.RPRN:
            seq = self.sequence(node)
        for s in seq:
            if isinstance(s, Assign):
                cid = TK.NAMEDTUPLE
            if not isinstance(s, Literal):
                is_literal = False
        self.consume(TK.RPRN)
        if len(seq) > 1:
            if seq[len(seq) - 1] is None:
                seq.pop()
            if is_literal:
                return lit_collection(cid, items=seq, loc=token.location)
            return Generate(cid, items=seq, loc=token.location)
        else:
            return List(items=seq, loc=token.location)

    def sequence(self, node=None):
        """EXPR <sep> EX1PR <sep> ..."""
        seq = [] if node is None else [node]
        while True:
            seq.append(self.expression())
            if not self.match1(TK.COMA):
                break
        return seq

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
        loc = self.tokens.location
        if self.peek().id == TK.RBRK:
            return List.EMPTY(loc=loc)
        while True:
            expr = self.expression()
            if not is_series:
                if expr.token.id in [TK.COLN, TK.DEFINE, TK.EQLS]:
                    is_series = True
            seq.append(expr)
            if not self.match1(TK.COMA):
                break
        node = Generate(target=(TK.SERIES if is_series else TK.LIST), items=seq, loc=loc)
        return node

    # return current token with provision for fetching if there are none.
    # after the first token, self.token works fine for peek.
    def peek(self, rel=0):
        tk = self.tokens.peek(rel=rel)
        return tk

    # returns current token and advances
    def advance(self):
        tk = self.tokens.read1()
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
        tk = self.peek()
        if tk.id == ex_tid:
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


def str2slice(s):
    if s.tid == TK.TIME:
        seq = s.lexeme.split(':')
        if len(seq) > 3:
            seq[2] = seq[3]
            del seq[3]
        elif len(seq) == 2:
            seq.append(1)
        elif len(seq) == 1:
            seq[2] = ''
            seq[3] = 1
        seq = [Int(x) if x is not '' else Literal.NONE() for x in seq]
        return seq
    return [None, None, None]
