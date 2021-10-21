# apply fixups to a parse tree

from abc import ABC

from exceptions import _expect, _expect_cl, _error, _expect_in_cl, _match_set, _contains_set
from tokens import TK, TCL, _IDENTIFIER_TYPES
from visitor import TreeFilter, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE

_fixupNodeTypeMappings = {
    'BinOp': BINARY_NODE,
    'Command': UNARY_NODE,
    'FnCall': BINARY_NODE,
    'Index': BINARY_NODE,
    'List': SEQUENCE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': 'Set',
    'UnaryOp': UNARY_NODE,
}


# fixups applied:
# sets with k:v pairs become dictionaries
# constant expression elimination
# empty sets?
#
class FixupSet2Dictionary(TreeFilter, ABC):
    def __init__(self, tree=None):
        super().__init__(tree, mapping=_fixupNodeTypeMappings, apply_parent_fixups=True)
        self._node_map = {}

    def apply(self):
        self.visit(self.tree.nodes)
        return self.tree

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        count = 0
        for n in list:
            count += 1
            print(f'\ntree:{count}')
            self.visit(n)

    def visit_Set(self, node, label=None):
        self.visit_sequence(node, label)
        values = node.values()
        if values is not None:
            d = {}
            k = 0
            if _contains_set(values, [TK.COLN, TK.ASSIGN]):
                for n in values:
                    if n is None:
                        continue
                    if _match_set(n, [TK.COLN, TK.ASSIGN]):
                        ident = _expect_in_cl(n.left, _IDENTIFIER_TYPES + [TCL.LITERAL])
                        key = ident.value
                        if key is not None:
                            if key not in d:
                                d[key] = n.right
                                continue
                            else:
                                _error(f'Duplicate Key: {key}', ident.token.location)
                    else:
                        d[f'%%key{k}:'] = n
                        k += 1
                node.value = d if len(d) > 0 else node.value

    # just for test: use DumpTree for proper printing
    def _print_node(self, node):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        id = ' '
        if getattr(node, 'parent', None) is not None:
            parent = node.parent
            id = f'{parent._num + 1}' if parent._num is not None else ' '
        print(f'{self._count:5d} : {indent}{node}: {node.token.format()}, parent:{id}')