# apply fixups to a parse tree

from abc import ABC

from visitor import TreeFilter


# fixups applied:
# sets with k:v pairs become dictionaries
#
class Fixup(TreeFilter, ABC):
    def __init__(self, tree=None):
        super().__init__(tree, apply_parent_fixups=True)

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        pass

    def apply(self):
        self.visit(self.tree.nodes)
        return self.tree
