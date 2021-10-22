from abc import ABC, abstractmethod

BINARY_NODE = 'visit_binary_node'
DEFAULT_NODE = 'visit_node'
NATIVE_VALUE = 'visit_intrinsic'
SEQUENCE_NODE = 'visit_sequence'
UNARY_NODE = 'visit_unary_node'
VALUE_NODE = 'visit_value'

_defaultNodeTypeMappings = {
    'BinOp': BINARY_NODE,
    'Command': UNARY_NODE,
    'FnCall': BINARY_NODE,
    'Index': BINARY_NODE,
    'List': SEQUENCE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': SEQUENCE_NODE,
    'UnaryOp': UNARY_NODE,
}


class NodeVisitor(object):
    def __init__(self, mapping=None):
        self.map2name = _defaultNodeTypeMappings if mapping is None else mapping

    def visit(self, node):
        if node is not None:
            label = type(node).__name__
            method_name = f'{self.node2name(label)}'
            visitor = getattr(self, method_name, None)
            if visitor is None:
                method_name = DEFAULT_NODE
                visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node, label)

    def generic_visit(self, node, label=None):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def node2name(self, name):
        if self.map2name is not None and name is not None:
            label = name if name not in self.map2name else self.map2name[name]
            return label
        return name


# a tree filter applies some operation to every node in the tree (pre-order).
class TreeFilter(NodeVisitor, ABC):

    def __init__(self, mapping=None, apply_parent_fixups=True):
        super().__init__(mapping)
        self.tree = None
        self.apply_parent_fixups = apply_parent_fixups
        self._count = 0
        self._depth = 0

    @abstractmethod
    def apply(self, tree=None):
        self._count = 0
        pass  # must return tree

    @abstractmethod
    def visit_node(self, node, label=None):
        node._num = self._count
        self._count += 1

    def visit_tuple(self, node, label=None):
        print(f'{node}')

    # helpers
    def visit_binary_node(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        if self.apply_parent_fixups:
            if node.left is not None:
                node.left.parent = node
            if node.right is not None:
                node.right.parent = node
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_sequence(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        values = node.values()
        if values is None:
            return node
        for idx in range(0, len(values)):
            n = values[idx]
            if n is None:
                continue
            n.parent = node if self.apply_parent_fixups else n.parent
            self.visit(n)
        self.dedent()

    def visit_unary_node(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        if node is not None and node.expr is not None:
            node.expr.parent = node if self.apply_parent_fixups else node.expr.parent
        self.visit(node.expr)
        self.dedent()

    def visit_value(self, node, label=None):
        return self.visit_node(node, label)

    def indent(self):
        self._depth += 1
        return

    def dedent(self):
        self._depth -= 1
