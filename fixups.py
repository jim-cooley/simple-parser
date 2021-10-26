# apply fixups to a parse tree

from abc import ABC

from evaluate import negate_literal, increment_literal, decrement_literal, not_literal
from literals import List
from modifytree import TreeModifier
from scope import Scope
from tokens import TK, TCL, Token
from visitor import BINARY_NODE

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
    'UnaryOp': 'process_unops',
}


# fixups applied:
# sets with TK.ASSIGN -> TK.TUPLE
# parameter lists with TK.ASSIGN -> TK.TUPLE
# :<assignment> -> :<parameter_list>(<assign>)
# symbol scoping
# constant expression elimination
#

class Fixups(TreeModifier, ABC):
    keywords = None
    global_symbols = None
    symbols = None
    _print_nodes = False

    def __init__(self, environment):
        super().__init__(mapping=_fixupNodeTypeMappings, apply_parent_fixups=True)
        self.environment = environment

    def apply(self, trees):
        self._init(trees)
        if trees is None:
            return None
        for t in trees:
            self.visit(t.root)
        return self.trees

    # overridden:
    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        return node

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        for idx in range(0, len(list)):
            n = list[idx]
            if n is None:
                continue
            if self._print_nodes:
                print(f'\ntree:{idx+1}')
            list[idx] = self.visit(n)
        return list

    def convert_coln_plist(self, node, label=None):
        if node is not None:
            if node.token.id == TK.TUPLE:
                if node.left is not None and node.left.token.id == TK.ASSIGN:
                    node.left = _fixup_coln_plist(node, node.left)
                if node.right is not None and node.right.token.id == TK.ASSIGN:
                    node.right = _fixup_coln_plist(node, node.right)
            return self.visit_binary_node(node, label)
        return node

    def convert_tuples(self, node, label=None):
        rnode = self.visit_sequence(node, label)
        values = node.values()
        if values is not None:
            for n in values:
                if n is None:
                    continue
                if n.token.id == TK.ASSIGN:
                    n.token.id = TK.TUPLE
        return rnode

    def process_binops(self, node, label=None):
        rnode = self.visit_binary_node(node, label)
        if node is not None:
            tkid = node.token.id
            if tkid == TK.TUPLE:
                return self.convert_coln_plist(node, label)
        return rnode

    def process_command(self, node, label=None):
        op = node.expr
        if op is not None:
            if op.token.t_class == TCL.BINOP:
                command = op.left.token.lexeme
                expr = op.right
                print(f'command: {node.token.lexeme}{command}: {expr}')
                node.token.lexeme = f'%%{command}'
                node.token.value = command
        return self.visit_unary_node(node, label)

    def process_unops(self, node, label=None):
        if node is None:
            return None
        node.expr = self.visit(node.expr)
        expr = node.expr
        if expr is None:
            return node
        if expr.token.t_class == TCL.LITERAL:
            if node.op == TK.NEG:
                negate_literal(expr)
                return _lift(node, expr)
            elif node.op == TK.POS:
                return _lift(node, expr)
            elif node.op == TK.INCREMENT:
                increment_literal(expr)
                return _lift(node, expr)
            elif node.op == TK.DECREMENT:
                decrement_literal(expr)
                return _lift(node, expr)
            elif node.op == TK.NOT:
                not_literal(expr)
                return _lift(node, expr)
        return node

    def print_symbols(self):
        if self.global_symbols is not None:
            print(f'\n\nsymbol table:')
            self.global_symbols.printall(indent=1)

    def _init(self, tree):
        self.trees = tree
        self.keywords = self.environment.keywords
        self.globals = self.environment.globals

# just for test: use DumpTree for proper printing
    def _print_node(self, node):
        if self._print_nodes:
            indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
            id = ' '
            if getattr(node, 'parent', None) is not None:
                parent = node.parent
                id = f'{parent._num + 1}' if parent._num is not None else ' '
            print(f'{self._count:5d} : {indent}{node}: {node.token.format()}, parent:{id}')


def _lift(node, child):
    parent = node.parent
    child.parent = parent
    return child


# fixup helpers:
def _fixup_coln_plist(node, target):
    plist = List(Token(TK.PARAMETER_LIST, tcl=TCL.LIST, lex='(', loc=node.token.location), [target])
    target.parent = plist
    plist.parent = node
    return plist
