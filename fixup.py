# apply fixups to a parse tree

from abc import ABC

from visitor import TreeFilter, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, DEFAULT_NODE

_fixupNodeTypeMappings = {
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


# fixups applied:
# sets with k:v pairs become dictionaries
#
class Fixup(TreeFilter, ABC):
    def __init__(self, tree=None):
        super().__init__(tree, mapping=_fixupNodeTypeMappings, apply_parent_fixups=True)

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        pass

    def apply(self):
        self.visit(self.tree.nodes)
        return self.tree
