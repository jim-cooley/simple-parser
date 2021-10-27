from environment import Environment
from evaluate import evaluate_literal, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set
from scope import Scope
from visitor import TreeFilter, BINARY_NODE, VALUE_NODE, SEQUENCE_NODE, DEFAULT_NODE, UNARY_NODE, NATIVE_VALUE

_visitNodeTypeMappings = {
    'BinOp': 'process_binops',
    'Bool': 'visit_literal',
    'Command': UNARY_NODE,
    'DateDiff': 'visit_literal',
    'DateTime': 'visit_literal',
    'Duration': 'visit_literal',
    'Float': 'visit_literal',
    'FnCall': BINARY_NODE,
    'Ident': 'visit_ident',
    'Index': BINARY_NODE,
    'Int': 'visit_literal',
    'List': SEQUENCE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': 'visit_literal',
    'PropCall': BINARY_NODE,
    'PropRef': 'process_binops',
    'Set': 'process_set',
    'Str': 'visit_literal',
    'Time': 'visit_literal',
    'UnaryOp': UNARY_NODE,

    'list': 'visit_list',
#   'int': 'process_intrinsic',
#   'str': 'process_intrinsic',
}


class Interpreter(TreeFilter):

    def __init__(self, environment):
        super().__init__(mapping=_visitNodeTypeMappings, apply_parent_fixups=True)
        self.environment = environment
        self._verbose = False

    def apply(self, tree=None):
        self.trees.values = self.visit(self.trees.root)
        return self.trees

    def apply(self, trees):
        self._init(trees)
        if trees is None:
            return None
        for t in trees:
            t.values = self.visit(t.root)
        return self.trees

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        return node.value

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        count = 0
        values = []
        for n in list:
            count += 1
            if self._verbose:
                print(f'\ntree:{count}')
            values.append(self.visit(n))
        return values

    def visit_literal(self, node, label=None):
        return evaluate_literal(node)

    def visit_ident(self, node, label=None):
        return evaluate_identifier(node)

    def visit_intrinsic(self, value, label=None):
        return value

    def process_binops(self, node, label=None):
        node.left.value = self.visit(node.left)
        node.right.value = self.visit(node.right)
        return evaluate_binary_operation(node)

    def process_set(self, node, label=None):
        if node is None:
            return None
        values = node.values()
        if values is None:
            return None
        return evaluate_set(node, self)

    def process_unops(self, node, label=None):
        if node is None:
            return None
        self.visit(node.expr)
#        if expr.token.t_class == TCL.LITERAL:
#            if node.op == TK.NOT:
#                expr = not_literal(expr)
#                return _lift(node, expr)
#            elif node.op == TK.INCREMENT:
#                 expr = increment_literal(expr)
#                 return _lift(node, expr)
#             elif node.op == TK.DECREMENT:
#                 expr = decrement_literal(expr)
#                 return _lift(node, expr)
#             elif node.op == TK.NEG:
#                 expr = negate_literal(expr)
#                 return _lift(node, expr)
#             elif node.op == TK.POS:
#                 return _lift(node, expr)
        return node

    def _init(self, tree):
        self.trees = tree
        self.keywords = self.environment.keywords
        self.globals = self.environment.globals

    def print_symbols(self):
        if self._verbose:
            if self.symbols is not None:
                print(f'\n\nsymbol table:')
                self.symbols.printall(indent=1)

    def _print_node(self, node):
        if self._verbose:
            indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
            id = ' '
            if getattr(node, 'parent', None) is not None:
                parent = node.parent
                id = f'{parent._num + 1}' if parent._num is not None else ' '
            print(f'{self._count:5d} : {indent}{node}: {node.token.format()}, parent:{id}')

