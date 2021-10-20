from abc import ABC, abstractmethod


class NodeVisitor(object):
    def visit(self, node):
        if node is not None:
            method_name = 'visit_' + type(node).__name__
            visitor = getattr(self, method_name, None)
            if visitor is None:
                method_name = 'visit_Node'
                visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


# a tree filter will visit every node of the tree (pre-order).
class TreeFilter(NodeVisitor, ABC):
    def __init__(self, tree=None, apply_parent_fixups=True):
        self.tree = tree
        self.apply_parent_fixups = apply_parent_fixups
        self._ncount = 0

    # structural visitation
    def visit_list(self, list):
        count = 0
        for n in list:
            count += 1
            print(f'tree{count}')
            self.visit(n)

    def visit_Seq(self, node):
        self.visit_Node(node)
        for n in node.sequence():
            if n is None:
                continue
            n.parent = node
            self.visit(n)

    def visit_BinOp(self, node):
        self.visit_Node(node)
        self.visit(node.left)
        self.visit(node.right)

    def visit_Set(self, node):
        self.visit_Node(node)
        if node.value is not None:
            if node.value.sequence() is not None:
                for n in node.value.sequence():
                    if n is None:
                        continue
                    n.parent = node
                    self.visit(n)

    @abstractmethod
    def visit_Node(self, node):
        self._ncount += 1
        _print_node(self._ncount, node)
        pass

    @abstractmethod
    def apply(self):
        self._ncount = 0
        pass    # must return tree


def _print_node(count, node):
    print(f'{count}: {node}: TK.{node.token.id.name}')
