
#
# Perform a Postfix notational print of the tree
#
from enum import IntEnum

from tokens import TK, TCL, TK_ASSIGN
from visitor import TreeFilter, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, NATIVE_LIST, ASSIGNMENT_NODE, VALUE_NODE, \
    DEFAULT_NODE, NATIVE_VALUE


class GRP(IntEnum):
    OPEN = 0
    CLOSE = 2
    SEP = 1
    EMPTY = 3


_tk2pfx = {
    TK.ADD: 'add',  # +
    TK.ALL: 'all',  # all:
    TK.AND: 'and',
    TK.ANY: 'any',  # any:
    TK.APPLY: 'apply',  # >>
    TK.ASSIGN: 'assign',  # =
    TK.BLOCK: 'scope',
    TK.BOOL: 'b',
    TK.BUY: 'buy',
    TK.CHAIN: 'chain',
    TK.COEQ: 'def',
    TK.COMMAND: 'command',
    TK.COMPARE: 'cmp',
    TK.DECREMENT: 'decr',  # --
    TK.DEF: '_def',
    TK.DEFINE: 'def',
    TK.DIV: 'div',  # /
    TK.DUR: 'dur',
    TK.EMPTY: 'ø',  # empty set
    TK.EQLS: 'assign',
    TK.EVENT: 'event',  # from =>
    TK.FALL_BELOW: 'fall',  # <|
    TK.FALSE: 'b',
    TK.FLOT: 'f',
    TK.FUNCTION: 'fn',
    TK.GTE: 'is_gte',
    TK.GTR: 'is_gt',
    TK.IN: 'in',
    TK.INCREMENT: 'incr',
    TK.INDEX: 'idx',  # indexing expression
    TK.INT: 'i',
    TK.ISEQ: 'is_eq',  # ==
    TK.KVPAIR: 'kv',  # key:value
    TK.LESS: 'is_lt',
    TK.LIST: '_',
    TK.LTE: 'is_lte',
    TK.MNEQ: 'subeq',
    TK.MUL: 'mul',  # *
    TK.NEG: 'neg',  # unary - (negate)
    TK.NEQ: 'is_ne',
    TK.NONE: 'lit',
    TK.NONEOF: 'noneof',  # none:
    TK.NOT: 'not',
    TK.NOW: 'now',
    TK.OR: 'or',
    TK.PCT: 'f',
    TK.PLEQ: 'addeq',
    TK.POS: 'pos',  # unary +
    TK.POW: 'pow',  # ^
    TK.PRODUCE: 'raise',  # =>
    TK.RANGE: 'range',
    TK.REF: 'ref',
    TK.RISE_ABOVE: 'rise',  # >|
    TK.SELL: 'sell',
    TK.SET: 'set',
    TK.SIGNAL: 'signal',
    TK.STR: 'str',
    TK.SUB: 'sub',  # - (subtract)
    TK.TIME: 'time',
    TK.TODAY: 'today',
    TK.TRUE: 'b',
    TK.TUPLE: '',
    TK.VAR: 'var',
}

_tk2grp = {
    TK.INDEX:['[ ', ', ', ' ]', '[]'],
    TK.LIST: ['[', ', ', ']', '[]'],
    TK.CHAIN: ['{', ' | ', '}', '{}'],
    TK.SET: ['{ ', ', ',  ' }', '{}'],
    TK.TUPLE: ['( ', ', ', ' )', '()']
}

_DEFAULT_GRP = ['( ', ', ', ' )', '()']

_DEFINITION_NODE = 'visit_define_node'

_postfixNodeTypeMappings = {
    'ApplyChainProd': ASSIGNMENT_NODE,
    'Assign': ASSIGNMENT_NODE,
    'BinOp': BINARY_NODE,
    'Block': SEQUENCE_NODE,
    'Bool': VALUE_NODE,
    'Command': UNARY_NODE,
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
    'Define': _DEFINITION_NODE,
    'DefineChainProd': _DEFINITION_NODE,
    'DefineFn': _DEFINITION_NODE,
    'DefineVar': _DEFINITION_NODE,
    'DefineVarFn': _DEFINITION_NODE,
    'Duration': VALUE_NODE,
    'Float': VALUE_NODE,
    'Flow': SEQUENCE_NODE,
    'FnCall': BINARY_NODE,
    'Get': VALUE_NODE,
    'Ident': VALUE_NODE,
    'Index': BINARY_NODE,
    'Int': VALUE_NODE,
    'List': SEQUENCE_NODE,
    'Literal': VALUE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': SEQUENCE_NODE,
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'UnaryOp': UNARY_NODE,
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
    'list': NATIVE_LIST,
}


class NotationPrinter(TreeFilter):

    def __init__(self):
        super().__init__(mapping=_postfixNodeTypeMappings, apply_parent_fixups=True)
        self._depth = 0
        self._indent = True
        self._notes = []
        self._print_end = '' if self._indent is False else '\n'

    def apply(self, tree=None):
        self._notes = []
        self.visit(tree)
        self._depth = 0
        return self._print_end.join(self._notes)

    def indent(self):
        self._depth += 1

    def dedent(self):
        self._depth -= 1

    # default
    def visit_node(self, node, label=None):
        self._print_notation(node)

    def visit_assignment_node(self, node, label=None):
        self._print_notation_token(TK_ASSIGN)
        self._print_append(_get_grouping(node.token, GRP.OPEN))
        if node.op == TK.EQLS:
            self._print_indented(f'{node.token.lexeme}, ')
        else:
            self._print_indented(f'{_tk2pfx[node.op]}, {node.token.lexeme}, ')
        if node is not None and node.right is not None:
            self.indent()
            self.visit(node.right)
            self.dedent()
        self._print_indented(_get_grouping(node.token, GRP.CLOSE))

    def visit_binary_node(self, node, label=None):
        self.visit_node(node, label)
        self._print_indented(_get_grouping(node.token, GRP.OPEN))
        self.indent()
        self.visit(node.left)
        if not self._indent:
            self._print_indented(_get_grouping(node.token, GRP.SEP))
        self.visit(node.right)
        self._print_indented(_get_grouping(node.token, GRP.CLOSE))
        self.dedent()

    def visit_define_node(self, node, label=None):
        self._print_indented(f'{node.token.lexeme} := ')
        self._print_append(_get_grouping(node.token, GRP.OPEN))
        self.indent()
        if node is not None and node.right is not None:
            self.visit(node.right)
        self.dedent()
        self._print_indented(_get_grouping(node.token, GRP.CLOSE))

    def visit_intrinsic(self, node, label=None):
        self.visit_node(node, label)

    def visit_list(self, trees, label=None):
        raise Exception("Invalid list of roots passed to apply.")

    def visit_sequence(self, node, label=None):
        self.visit_node(node, label)
        values = node.values()
        if values is None:
            return node
        _len = len(values)
        if _len != 0:
            self._print_append(_get_grouping(node.token, GRP.OPEN))
            self.indent()
            for idx in range(0, _len):
                n = values[idx]
                if n is None:
                    continue
                self.visit(n)
                if idx < _len - 1:
                    if not self._indent:
                        self._print_indented(_get_grouping(node.token, GRP.SEP))
            self.dedent()
            self._print_indented(_get_grouping(node.token, GRP.CLOSE))
        else:
            self._print_indented(_get_grouping(node.token, GRP.EMPTY))

    def visit_unary_node(self, node, label=None):
        self.visit_node(node, label)
        self._print_append(_get_grouping(node.token, GRP.OPEN))
        if node is not None and node.expr is not None:
            self.indent()
            self.visit(node.expr)
            self.dedent()
        self._print_indented(_get_grouping(node.token, GRP.CLOSE))

    def visit_value_node(self, node, label=None):
        self.visit_node(node, label)

    def _print_notation(self, node):
        self._print_notation_token(node.token)

    def _print_indented(self, note):
        indent = '' if self._indent is False or self._depth < 1 else ' '.ljust(self._depth * 4)
        self._notes.append(f'{indent}{note}')

    def _print_append(self, note):
        self._notes[len(self._notes) - 1] += note

    def _print_notation_token(self, token):
        val = ''
        if token is not None:
            val = f'{_tk2pfx[token.id]}' if token.id in _tk2pfx else token.lexeme
            if token.id not in [TK.LIST, TK.SET] and token.t_class == TCL.LITERAL:
                v = f'{token.value}'
                val = f'{val}({v.lower()})'
        self._print_indented(f'{val}')


def _get_grouping(token, grp):
    if token is not None:
        if token.id in _tk2grp:
            return _tk2grp[token.id][grp]
    return _DEFAULT_GRP[grp]
