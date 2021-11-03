
#
# Perform a Postfix functional notational print of the tree
#
from enum import IntEnum

from literals import Set
from tokens import TK, TCL, _tk2glyph
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
    TK.APPLY: 'apply>',  # >>
    TK.ASSIGN: 'assign',  # =
    TK.BLOCK: 'block',
    TK.BOOL: 'b',
    TK.BUY: 'buy',
    TK.CHAIN: 'chain',
    TK.COEQ: 'def_fn',
    TK.COLN: 'coln:',
    TK.COMMAND: 'command',
    TK.COMPARE: 'cmp',
    TK.DECREMENT: 'decr',  # --
    TK.DEF: '_def',
    TK.DEFINE: 'def',
    TK.DIV: 'div',  # /
    TK.DOT: '.ref',
    TK.DUR: 'dur',
    TK.EMPTY: 'Ø',  # empty set
    TK.EQGT: 'assign=>',
    TK.EQLS: 'assign=',
    TK.EVENT: 'event',  # from =>
    TK.FALL_BELOW: 'if_below',  # <|
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
    TK.LBRC: '{',
    TK.LESS: 'is_lt',
    TK.LIST: 'list',
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
    TK.PRODUCE: 'produce',  # =>
    TK.RANGE: 'range',
    TK.REF: 'ref',
    TK.RISE_ABOVE: 'if_above',  # >|
    TK.SELL: 'sell',
    TK.SET: 'set',
    TK.SIGNAL: 'signal',
    TK.STR: 'str',
    TK.SUB: 'sub',  # - (subtract)
    TK.TIME: 'time',
    TK.TODAY: 'today',
    TK.TRUE: 'b',
    TK.TUPLE: 'tup',
    TK.VAR: 'var',
}

_tk2grp = {
    TK.CHAIN: ['{', ' | ', '}', '{}'],
    TK.EMPTY: ['{', ', ',  '}', 'Ø'],
    TK.INDEX:['[', ', ', ']', '[]'],
    TK.LIST: ['[', ', ', ']', '[]'],
    TK.SET: ['{', ', ',  '}', '{}'],
    TK.TUPLE: ['(', ', ', ')', '()']
}

_DEFAULT_GRP = ['(', ', ', ')', '()']

_DEFINITION_NODE = 'visit_define_node'
_FUNCTION_NODE = 'visit_function_call'
_IDENT_NODE = 'visit_identifier'

_postfixNodeTypeMappings = {
    'ApplyChainProd': _DEFINITION_NODE,
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
    'FnCall': _FUNCTION_NODE,
    'Get': VALUE_NODE,
    'Ident': _IDENT_NODE,
    'Index': BINARY_NODE,
    'Int': VALUE_NODE,
    'List': SEQUENCE_NODE,
    'Literal': VALUE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Ref': VALUE_NODE,
    'Set': SEQUENCE_NODE,
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'UnaryOp': UNARY_NODE,
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
    'list': NATIVE_LIST,
}


class FunctionalNotationPrinter(TreeFilter):

    def __init__(self):
        super().__init__(mapping=_postfixNodeTypeMappings, apply_parent_fixups=True)
        self._depth = 0
        self._indent = False
        self._notes = []
        self._print_end = '' if self._indent is False else '\n'
        self._append = False

    def apply(self, tree=None):
        self._notes = []
        self._depth = 1
        self.visit(tree)
        return self._print_end.join(self._notes)

    def set_append(self, append):
        a = self._append
        self._append = append
        return a

    def indent(self):
        self._depth += 1

    def dedent(self):
        self._depth -= 1

    # default
    def visit_node(self, node, label=None):
        self._print_notation(node)

    def visit_assignment_node(self, node, label=None):
        self._print_indented(f'{_tk2pfx[node.op]}')
        self._process_binary_node(node)

    def visit_binary_node(self, node, label=None):
        self.visit_node(node, label)
        self._process_binary_node(node)

    def visit_define_node(self, node, label=None):
        text = f'{label.lower()}{_tk2glyph[node.op]} ' if node.op in _tk2glyph else f'{label.lower()} '
        self._print_indented(text)
        self._process_binary_node(node)

    def _process_binary_node(self, node):
        self._print_open(node.token, append=True)
        self.indent()
        self.visit(node.left)
        self._print_sep(node.token, append=True)
        self.visit(node.right)
        self.dedent()
        self._print_close(node.token)

    def visit_function_call(self, node, label=None):
        self._print_indented(f'fn')
        self._print_open(node.token, append=True)
        self.indent()
        self.visit(node.left)
        self._print_sep(node.token, append=True)
        self.visit(node.right)
        self.dedent()
        self._print_close(node.token)

    def visit_ident_node(self, node, label=None):
        self.visit_node(node, label)

    def visit_intrinsic(self, node, label=None):
        self.visit_node(node, label)

    def visit_list(self, trees, label=None):
        raise Exception("Invalid list of roots passed to apply.")

    def visit_sequence(self, node, label=None):
        self._print_indented(f'{_tk2pfx[node.token.id]}')
        values = node.values()
        if values is None:
            return node
        _len = len(values)
        if _len != 0:
            self._print_open(node.token, append=True)
            self.indent()
            for idx in range(0, _len):
                n = values[idx]
                if n is None:
                    continue
                self.visit(n)
                if idx < _len - 1:
                    self._print_sep(node.token, append=True)
            self.dedent()
            self._print_close(node.token)
        elif not isinstance(node, Set):
            self._print_empty(node.token)

    def visit_unary_node(self, node, label=None):
        self.visit_node(node, label)
        self._print_open(node.token, append=True)
        if node is not None and node.expr is not None:
            self.indent()
            self.visit(node.expr)
            self.dedent()
        self._print_close(node.token)

    def visit_value_node(self, node, label=None):
        self.visit_node(node, label)

    def _print(self, note, append=None):
        append = append if append is not None else self._append
        if append:
            self._print_append(note)
        else:
            self._print_indented(note)

    def _print_append(self, note):
        self._notes[len(self._notes) - 1] += note

    def _print_indented(self, note):
        indent = '' if self._indent is False or self._depth < 1 else ' '.ljust(self._depth * 4)
        note = f'{indent}{note}'
        self._notes.append(note)

    def _print_notation(self, node, append=None):
        self._print_notation_token(node.token, append=append)

    def _print_notation_token(self, token, append=None):
        val = ''
        if token is not None:
            val = f'{_tk2pfx[token.id]}' if token.id in _tk2pfx else token.lexeme
            if token.id not in [TK.LIST, TK.SET] and token.t_class == TCL.LITERAL:
                v = f'{token.value}'
                val = f'{val}({v.lower()})'
        self._print(f'{val}', append=append)

    def _print_open(self, tk, append=None):
        self._print(f'{_get_grouping(tk, GRP.OPEN)} ', append=append)

    def _print_sep(self, tk, append=None):
        self._print(f'{_get_grouping(tk, GRP.SEP)}', append=append)

    def _print_close(self, tk, append=None):
        pad = '' if self._indent else ' '
        self._print(f'{pad}{_get_grouping(tk, GRP.CLOSE)}', append=append)

    def _print_empty(self, tk, append=None):
        self._print(f'{_get_grouping(tk, GRP.EMPTY)}', append=append)


def _get_grouping(token, grp):
    if token is not None:
        if token.id in _tk2grp:
            return _tk2grp[token.id][grp]
    return _DEFAULT_GRP[grp]