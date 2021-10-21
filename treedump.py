import tokens as _
from visitor import NodeVisitor, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, DEFAULT_NODE, VALUE_NODE, NATIVE_VALUE

_nodeTypeMappings = {
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
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
}


class DumpTree(NodeVisitor):
    def __init__(self):
        super().__init__(_nodeTypeMappings)
        self._ncount = 1
        self._body = []
        self._depth = 0

    def indent(self):
        self._depth += 1

    def dedent(self):
        self._depth -= 1

    def dump(self, tree):
        self.visit(tree)
        return self._body

    def format_indent(self):
        return '' if self._depth < 1 else ' '.ljust(self._depth * 4)

    # helpers
    def visit_intrinsic(self, value, label=None):
        self._print_object(value, label)
        self._ncount += 1

    def visit_tuple(self, node, label=None):
        self._visit_sequence(node)

    def visit_binary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_sequence(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        if node.value is not None:
            self._visit_sequence(node.values())

    def _visit_sequence(self, li, label=None):
        self.indent()
        if len(li) != 0:
            for n in li:
                if n is not None:
                    self.visit(n)
        self.dedent()

    def visit_unary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.expr)
        self.dedent()

    def visit_value(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1

    def _print_object(self, obj, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        line = '{:5d} : {}{} {}'.format(self._ncount, indent, label, obj)
        self._body.append(line)

    def _print_node(self, node, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        line = '{:5d} : {}{} {}'.format(self._ncount, indent, label, node.token.format())
        self._body.append(line)
