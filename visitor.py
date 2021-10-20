from abc import ABC, abstractmethod

BINARY_NODE = 'binary_node'
DEFAULT_NODE = 'node'
SEQUENCE_NODE = 'sequence'
UNARY_NODE = 'unary_node'
VALUE_NODE = 'value'

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
            method_name = f'visit_{self.node2name(label)}'
            visitor = getattr(self, method_name, None)
            if visitor is None:
                method_name = 'visit_node'
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
    def __init__(self, tree=None, mapping=None, apply_parent_fixups=True):
        super().__init__(mapping)
        self.tree = tree
        self.apply_parent_fixups = apply_parent_fixups
        self._ncount = 0
        self._depth = 0

    @abstractmethod
    def apply(self):
        self._ncount = 0
        pass  # must return tree

    @abstractmethod
    def visit_node(self, node, label=None):
        self._ncount += 1
        self._print_node(node)
        pass

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

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        count = 0
        for n in list:
            count += 1
            print(f'tree{count}')
            self.visit(n)

    def visit_sequence(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        values = node.values()
        if values is None:
            return
        for n in values:
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
        self.visit_node(node, label)

    def indent(self):
        self._depth += 1
        return

    def dedent(self):
        self._depth -= 1

    # just for test: use DumpTree for proper printing
    def _print_node(self, node):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        print(f'{self._ncount:5d} : {indent}{node}: {node.token.format()}')
