# apply fixups to a parse tree

from abc import ABC

from literals import List
from tokens import TK, TCL, Token
from visitor import TreeFilter, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE

_fixupNodeTypeMappings = {
    'BinOp': 'process_binops',
    'Command': 'process_command',
    'FnCall': BINARY_NODE,
    'Index': BINARY_NODE,
    'list': 'visit_list',
    'List': 'convert_tuples',
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Set': 'convert_tuples',
    'UnaryOp': UNARY_NODE,
}


# fixups applied:
# sets with TK.ASSIGN -> TK.TUPLE
# parameter lists with TK.ASSIGN -> TK.TUPLE
# :<assignment> -> :<parameter_list>(<assign>)
# symbol scoping
# constant expression elimination
#

class FixupSet2Dictionary(TreeFilter, ABC):
    def __init__(self, tree=None, print=False):
        super().__init__(tree, mapping=_fixupNodeTypeMappings, apply_parent_fixups=True)
        self._node_map = {}
        self._print_nodes=print
        self.global_symbols = self.tree.keywords
        self.current_scope = None
        self.symbols = self.global_symbols

    def apply(self, tree=None):
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
            if self._print_nodes:
                print(f'\ntree:{count}')
            self.visit(n)

    def convert_coln_plist(self, node, label=None):
        if node is not None:
            if node.token.id == TK.TUPLE:
                if node.left is not None and node.left.token.id == TK.ASSIGN:
                    node.left = _fixup_coln_plist(node, node.left)
                if node.right is not None and node.right.token.id == TK.ASSIGN:
                    node.right = _fixup_coln_plist(node, node.right)
            self.visit_binary_node(node, label)

    def convert_tuples(self, node, label=None):
        self.visit_sequence(node, label)
        values = node.values()
        if values is not None:
            for n in values:
                if n is None:
                    continue
                if n.token.id == TK.ASSIGN:
                    n.token.id = TK.TUPLE

    def process_binops(self, node, label=None):
        if node is not None:
            tkid = node.token.id
            if tkid == TK.TUPLE:
                self.convert_coln_plist(node, label)

    def process_command(self, node, label=None):
        op = node.expr
        if op is not None:
            if op.token.t_class == TCL.BINOP:
                command = op.left.token.lexeme
                expr = op.right
                print(f'command: {node.token.lexeme}{command}: {expr}')
                node.token.lexeme = f'%%{command}'
                node.token.value = command
        self.visit_unary_node(node, label)

    def print_symbols(self):
        if self.global_symbols is not None:
            print(f'\n\nsymbol table:')
            self.global_symbols.print(indent=1)

    # just for test: use DumpTree for proper printing
    def _print_node(self, node):
        if self._print_nodes:
            indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
            id = ' '
            if getattr(node, 'parent', None) is not None:
                parent = node.parent
                id = f'{parent._num + 1}' if parent._num is not None else ' '
            print(f'{self._count:5d} : {indent}{node}: {node.token.format()}, parent:{id}')


# fixup helpers:
def _fixup_coln_plist(node, target):
    plist = List(Token(TK.PARAMETER_LIST, tcl=TCL.LIST, lex='(', loc=node.token.location), [target])
    target.parent = plist
    plist.parent = node
    return plist
