# apply fixups to a parse tree

from abc import ABC

from conversion import c_unbox, c_type, c_box
from eval_binops import eval_binops_dispatch_fixup
from eval_unary import decrement_literal, increment_literal, negate_literal, not_literal
from evaluate import _INTRINSIC_VALUE_TYPES
from tree import AST, Define, DefineVar, DefineFn, DefineVarFn
from literals import List, Literal, Bool
from modifytree import TreeModifier
from tokens import TK, TCL, Token
from visitor import BINARY_NODE, NATIVE_LIST, DEFAULT_NODE, VALUE_NODE, SEQUENCE_NODE

_FUNCTION_NODE = BINARY_NODE
_IDENT_NODE = 'visit_identifier'
_NATIVE_VALUE = 'visit_node'
_VISIT_DEFINITION = 'visit_definition'
ASSIGNMENT_NODE = 'visit_assignment'

BINARY_NODE = 'process_binops'

_fixupNodeTypeMappings = {
    'ApplyChainProd': _VISIT_DEFINITION,
    'Assign': ASSIGNMENT_NODE,
    'BinOp': BINARY_NODE,
    'Block': SEQUENCE_NODE,
    'Bool': VALUE_NODE,
    'Command': 'process_command',
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
    'Define': _VISIT_DEFINITION,
    'DefineChainProd': _VISIT_DEFINITION,
    'DefineFn': _VISIT_DEFINITION,
    'DefineVar': _VISIT_DEFINITION,
    'DefineVarFn': _VISIT_DEFINITION,
    'Duration': VALUE_NODE,
    'Float': VALUE_NODE,
    'Flow': SEQUENCE_NODE,
    'FnCall': _FUNCTION_NODE,
    'Get': VALUE_NODE,
    'Ident': _IDENT_NODE,
    'Index': BINARY_NODE,
    'Int': VALUE_NODE,
    'List': 'convert_tuples',
    'Literal': VALUE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Ref': VALUE_NODE,
    'Set': 'convert_tuples',
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'UnaryOp': 'process_unops',
    'int': _NATIVE_VALUE,
    'str': _NATIVE_VALUE,
    'list': NATIVE_LIST,
}


# fixups applied:
# sets with TK.ASSIGN -> TK.TUPLE
# parameter lists with TK.ASSIGN -> TK.TUPLE
# :<assignment> -> :<parameter_list>(<assign>)
# symbol scoping
# constant expression elimination
#

class Fixups(TreeModifier, ABC):
    def __init__(self, environment):
        super().__init__(mapping=_fixupNodeTypeMappings, apply_parent_fixups=True)
        self.environment = environment
        self._print_nodes = False

    def apply(self, trees):
        self._init(trees)
        if trees is None:
            return None
        for t in trees:
            val = self.visit(t.root)
            if not isinstance(val, AST):
                val = Literal.lit(val)
            t.root = val
        return self.trees

    # overridden:
    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        return node

    # non-converting visitation
    def visit_assignment(self, node, label=None):
        return self.visit_binary_node(node, label)

    def visit_definition(self, node, label=None):
        return self.visit_binary_node(node, label)

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        for idx in range(0, len(list)):
            n = list[idx]
            if n is None:
                continue
            if self._print_nodes:
                print(f'\ntree:{idx + 1}')
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
            if node.left.token.t_class == TCL.LITERAL and node.right.token.t_class == TCL.LITERAL:
                rnode = _fixup_binary_operation(node)
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
        if node.expr is None:
            return node     # TODO: Probably a failure
        expr = node.expr
        l_tid = c_type(expr)
        l_value = c_unbox(expr)

        opid = node.op
        if expr.token.t_class == TCL.LITERAL:
            if opid == TK.NOT:
                l_value = not_literal(l_value, l_tid)
                return _lift(node, Bool(value=l_value, loc=expr.token.location))
            elif opid == TK.INCREMENT:
                l_value = increment_literal(l_value, l_tid)
                return _lift(node, Literal.lit(l_value, other=expr))
            elif opid == TK.DECREMENT:
                l_value = decrement_literal(l_value, l_tid)
                return _lift(node, Literal.lit(l_value, other=expr))
            elif opid == TK.NEG:
                l_value = negate_literal(l_value, l_tid)
                return _lift(node, Literal.lit(l_value, other=expr))
            elif opid == TK.POS:
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
    plist = List(Token(TK.TUPLE, tcl=TCL.TUPLE, lex='(', loc=node.token.location), [target])
    target.parent = plist
    plist.parent = node
    return plist


# no identifiers
def _fixup_binary_operation(node):
    op = node.op
    l_value = node.left.value
    l_ty = type(l_value).__name__
    r_value = node.right.value
    r_ty = type(r_value).__name__

    if l_value is None or r_value is None:
        return node

    if l_ty not in _INTRINSIC_VALUE_TYPES or r_ty not in _INTRINSIC_VALUE_TYPES:
        return node

    node.value = eval_binops_dispatch_fixup(node)
    return node
