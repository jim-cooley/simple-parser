from evaluate import evaluate_literal
from visitor import TreeFilter, BINARY_NODE, VALUE_NODE, SEQUENCE_NODE, DEFAULT_NODE, UNARY_NODE, NATIVE_VALUE

_visitNodeTypeMappings = {
    'BinOp': BINARY_NODE,
    'Bool': 'visit_literal',
    'Command': UNARY_NODE,
    'DateDiff': 'visit_literal',
    'DateTime': 'visit_literal',
    'Duration': 'visit_literal',
    'Float': 'visit_literal',
    'FnCall': BINARY_NODE,
    'Ident': VALUE_NODE,
    'Index': BINARY_NODE,
    'Int': 'visit_literal',
    'List': SEQUENCE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': 'visit_literal',
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': SEQUENCE_NODE,
    'Str': 'visit_literal',
    'Time': 'visit_literal',
    'UnaryOp': UNARY_NODE,

    'list': 'visit_list',
#   'int': 'process_intrinsic',
#   'str': 'process_intrinsic',
}


class Interpreter(TreeFilter):
    _node_map = {}
    keywords = None
    globals = None
    symbols = None
    _print_nodes = False

    def __init__(self):
        super().__init__(mapping=_visitNodeTypeMappings, apply_parent_fixups=True)

    def apply(self, tree=None):
        self._init(tree)
        self.tree.values = self.visit(self.tree.nodes)
        return self.tree

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        count = 0
        values = []
        for n in list:
            count += 1
            if self._print_nodes:
                print(f'\ntree:{count}')
            values.append(self.visit(n))
        return values

    def process_binops(self, node, label=None):
        if node is not None:
            tkid = node.token.id

    def visit_literal(self, node, label=None):
        return evaluate_literal(node)

    def visit_intrinsic(self, value, label=None):
        return value

    def process_unops(self, node, label=None):
        pass

    def _init(self, tree):
        self._node_map = {}
        self.tree = tree
        self.keywords = tree.keywords
        self.globals = tree.globals
        self.symbols = globals

    def print_symbols(self):
        if self.symbols is not None:
            print(f'\n\nsymbol table:')
            self.symbols.print(indent=1)

    def _print_node(self, node):
        if self._print_nodes:
            indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
            id = ' '
            if getattr(node, 'parent', None) is not None:
                parent = node.parent
                id = f'{parent._num + 1}' if parent._num is not None else ' '
            print(f'{self._count:5d} : {indent}{node}: {node.token.format()}, parent:{id}')

