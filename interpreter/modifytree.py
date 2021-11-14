# a tree filter that can modify the tree structure
from abc import ABC, abstractmethod

from interpreter.visitor import NodeVisitor


class TreeModifier(NodeVisitor, ABC):
    def __init__(self, mapping=None, apply_parent_fixups=True):
        super().__init__(mapping)
        self.apply_parent_fixups = apply_parent_fixups
        self._count = 0
        self._depth = 0

    @abstractmethod
    def apply(self, tree=None):
        self._count = 0
        return tree

    @abstractmethod
    def visit_node(self, node, label=None):
        node._num = self._count
        self._count += 1
        return node

    def visit_tuple(self, node, label=None):
        print(f'{node}')
        return node

    # helpers
    def visit_binary_node(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        if self.apply_parent_fixups:
            if node.left is not None:
                node.left.parent = node
            if node.right is not None:
                node.right.parent = node
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        self.dedent()
        return node

    def visit_sequence(self, node, label=None):
        if node is None:
            return None
        self.visit_node(node, label)
        self.indent()
        values = node.items()
        if values is None:
            return node
        for idx in range(0, len(values)):
            n = values[idx]
            if n is None:
                continue
            n.parent = node if self.apply_parent_fixups else n.parent
            values[idx] = self.visit(n)
        self.dedent()
        return node

    def visit_trinary_node(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        if self.apply_parent_fixups:
            if node.left is not None:
                node.left.parent = node
            if node.right is not None:
                node.right.parent = node
            if hasattr(node, 'args'):
                if node.args is not None:
                    node.args.parent = node
            else:
                if node.middle is not None:
                    node.middle.parent = node
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if hasattr(node, 'args'):
            node.args = self.visit(node.args)
        else:
            node.middle = self.visit(node.middle)
        self.dedent()
        return node

    def visit_unary_node(self, node, label=None):
        self.visit_node(node, label)
        self.indent()
        if node is not None and node.expr is not None:
            node.expr.parent = node if self.apply_parent_fixups else node.expr.parent
        self.visit(node.expr)
        self.dedent()
        return node

    def visit_value(self, node, label=None):
        return self.visit_node(node, label)

    def indent(self):
        self._depth += 1
        return

    def dedent(self):
        self._depth -= 1
