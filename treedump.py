import tokens as _
from visitor import NodeVisitor, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, DEFAULT_NODE, VALUE_NODE

_nodeNameMappings = {
    'BinOp': BINARY_NODE,
    'Bool': VALUE_NODE,
    'Command': UNARY_NODE,
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
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
}


class DumpTree(NodeVisitor):
    def __init__(self):
        super().__init__(_nodeNameMappings)
        self._ncount = 1
        self._body = []
        self._indent_level = 0
        self._indent = ''

    def indent(self):
        self._indent_level += 1
        self._indent = ' '.ljust(self._indent_level * 4)
        return

    def dedent(self):
        self._indent_level -= 1
        self._indent = ' '.ljust(self._indent_level * 4)

    def dump(self, tree):
        self.visit(tree)
        return self._body

    # node processing
    def visit_Duration(self, node, label='Dur'):
        self.visit_value(node, 'Dur')

    # helpers
    def visit_binary_node(self, node, label):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_sequence(self, node, label):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        if node.value is not None:
            self.indent()
            slist = node.values()
            if len(slist) != 0:
                for n in slist:
                    if n is not None:
                        self.visit(n)
            self.dedent()

    def visit_unary_node(self, node, label):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.expr)
        self.dedent()

    def visit_value(self, node, label):
        s = '{}node:{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
