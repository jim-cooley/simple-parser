# apply fixups to a parse tree

# fixups:
# sets with k:v pairs become dictionaries
from tree import NodeVisitor


class Fixup(NodeVisitor):
    def __init__(self, tree=None):
        self.tree = tree

    def visit_list(self, list):
        for n in list:
            self.visit(n)

    def visit_Seq(self, seq):
        _print_node(seq)
        for n in seq.sequence:
            self.visit(n)

    def visit_Set(self, s):
        _print_node(s)
        for n in s.sequence:
            self.visit(n)

    def visit_Node(self, node):
        _print_node(node)
        pass

    def apply(self):
        self.visit(self.tree.nodes)
        return self.tree


def _print_node(node):
    print(f'{node}: TK.{node.token.id.name}')
