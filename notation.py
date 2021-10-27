
#
# Perform a Postfix notational print of the tree
#
from enum import IntEnum

from tokens import TK, TCL
from visitor import TreeFilter, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, NATIVE_LIST


class GRP(IntEnum):
    OPEN = 0
    CLOSE = 2
    SEP = 1
    EMPTY = 3


_postfixNodeTypeMappings = {
    'BinOp': BINARY_NODE,
    'Command': UNARY_NODE,
    'FnCall': BINARY_NODE,
    'Index': BINARY_NODE,
    'List': SEQUENCE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': SEQUENCE_NODE,
    'UnaryOp': UNARY_NODE,
    'list': NATIVE_LIST,
}

_tk2pfx = {
    TK.ADD: 'add',  # +
    TK.ALL: 'all',  # all:
    TK.AND: 'and',
    TK.ANY: 'any',  # any:
    TK.APPLY: 'apply',  # >>
    TK.ASSIGN: 'assign',  # =
    TK.BOOL: 'b',
    TK.BUY: 'buy',
    TK.COMMAND: 'command',
    TK.COMPARE: 'cmp',
    TK.DECREMENT: 'decr', # --
    TK.DEFINE: 'def',
    TK.DIV: 'div',  # /
    TK.DUR: 'dur',
    TK.EMPTY: 'ø',  # empty set
    TK.EVENT: 'event',  # from =>
    TK.FALL_BELOW: 'fall',  # <|
    TK.FALSE: 'b',
    TK.FLOT: 'f',
    TK.FUNCTION: 'fn',
    TK.GTR: 'is_gt',
    TK.GTE: 'is_gte',
    TK.IN: 'in',
    TK.INCREMENT: 'incr',
    TK.INDEX: 'idx',  # indexing expression
    TK.INT: 'i',
    TK.ISEQ: 'is_eq',  # ==
    TK.LESS: 'is_lt',
    TK.LTE: 'is_lte',
    TK.LIST: '_',
    TK.MUL: 'mul',  # *
    TK.NEG: 'neg',  # unary - (negate)
    TK.NEQ: 'is_ne',
    TK.NONE: 'lit',
    TK.NONEOF: 'noneof',  # none:
    TK.NOT: 'not',
    TK.NOW: 'now',
    TK.OR: 'or',
    TK.PCT: 'f',
    TK.CHAIN: 'chain',
    TK.POS: 'pos',  # unary +
    TK.POW: 'pow',  # ^
    TK.RAISE: 'raise',  # =>
    TK.RANGE: 'range',
    TK.REF: 'ref',
    TK.RISE_ABOVE: 'rise',  # >|
    TK.SELL: 'sell',
    TK.SET: 'set',
    TK.SIGNAL: 'signal',
    TK.STR: 'str',
    TK.SUB: 'sub',  # - (subtract)
    TK.TODAY: 'today',
    TK.TIME: 'time',
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


class NotationPrinter(TreeFilter):
    _print_end = ''
    _notes = []

    def __init__(self):
        super().__init__(mapping=_postfixNodeTypeMappings, apply_parent_fixups=True)

    def apply(self, tree=None):
        self._notes = []
        self.visit(tree)
        return ''.join(self._notes)

    def visit_binary_node(self, node, label=None):
        self.visit_node(node, label)
        self._notes.append(_get_grouping(node.token, GRP.OPEN))
        self.visit(node.left)
        self._notes.append(_get_grouping(node.token, GRP.SEP))
        self.visit(node.right)
        self._notes.append(_get_grouping(node.token, GRP.CLOSE))

    def visit_list(self, trees, label=None):
        raise Exception("Invalid list of roots passed to apply.")

    def visit_node(self, node, label=None):
        self._print_notation(node)
        super().visit_node(node, label)

    def visit_sequence(self, node, label=None):
        self.visit_node(node, label)
        values = node.values()
        if values is None:
            return node
        _len = len(values)
        if _len != 0:
            self._notes.append(_get_grouping(node.token, GRP.OPEN))
            for idx in range(0, _len):
                n = values[idx]
                if n is None:
                    continue
                self.visit(n)
                if idx < _len - 1:
                    self._notes.append(_get_grouping(node.token, GRP.SEP))
            self._notes.append(_get_grouping(node.token, GRP.CLOSE))
        else:
            self._notes.append(_get_grouping(node.token, GRP.EMPTY))

    def visit_unary_node(self, node, label=None):
        self.visit_node(node, label)
        self._notes.append(_get_grouping(node.token, GRP.OPEN))
        if node is not None and node.expr is not None:
            self.visit(node.expr)
        self._notes.append(_get_grouping(node.token, GRP.CLOSE))

    def _print_notation(self, node):
        val = ''
        if node.token is not None:
            val = f'{_tk2pfx[node.token.id]}' if node.token.id in _tk2pfx else node.token.lexeme
            if node.token.t_class == TCL.LITERAL:
                v = f'{node.token.value}'
                val = f'{val}({v.lower()})'
        self._notes.append(f'{val}')


def _get_grouping(token, grp):
    if token is not None:
        if token.id in _tk2grp:
            return _tk2grp[token.id][grp]
    return _DEFAULT_GRP[grp]
