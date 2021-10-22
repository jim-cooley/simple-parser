from visitor import TreeFilter, BINARY_NODE, VALUE_NODE, SEQUENCE_NODE, DEFAULT_NODE, UNARY_NODE, NATIVE_VALUE

_visitNodeTypeMappings = {
    'BinOp': BINARY_NODE,
    'Bool': VALUE_NODE,
    'Command': UNARY_NODE,
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
    'Duration': VALUE_NODE,
    'Float': VALUE_NODE,
    'FnCall': BINARY_NODE,
    'Ident': VALUE_NODE,
    'Index': BINARY_NODE,
    'Int': VALUE_NODE,
    'List': SEQUENCE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': SEQUENCE_NODE,
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'UnaryOp': UNARY_NODE,

    'list': 'visit_list',
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
}


class Interpreter(TreeFilter):
    _node_map = {}
    keywords = None
    globals = None
    symbols = None
    _print_nodes = True

    def __init__(self):
        super().__init__(mapping=_visitNodeTypeMappings)

    def interpret(self):
        return self.apply(self.tree)

    def apply(self, tree=None):
        self.visit(self.tree.nodes)
        return self.tree

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        count = 0
        for n in list:
            count += 1
            if self._print_nodes:
                print(f'\ntree:{count}')
            self.visit(n)

    def _init(self, tree):
        self._node_map = {}
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

