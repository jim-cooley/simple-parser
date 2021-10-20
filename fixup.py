# apply fixups to a parse tree

from abc import ABC

from visitor import NodeVisitor, TreeFilter, _print_node


# fixups applied:
# sets with k:v pairs become dictionaries
#
class Fixup(TreeFilter, ABC):
    def __init__(self, tree=None):
        super().__init__(tree, apply_parent_fixups=True)

    def visit_Node(self, node):
        super().visit_Node(node)
        pass

    def apply(self):
        self.visit(self.tree.nodes)
        return self.tree
