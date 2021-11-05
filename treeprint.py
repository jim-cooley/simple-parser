import tokens as _
from notation_fn import FunctionalNotationPrinter
from environment import _t_print
from visitor import NodeVisitor, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, DEFAULT_NODE, VALUE_NODE, NATIVE_VALUE, \
    ASSIGNMENT_NODE

_nodeTypeMappings = {
    'ApplyChainProd': ASSIGNMENT_NODE,
    'Assign': ASSIGNMENT_NODE,
    'BinOp': BINARY_NODE,
    'Block': SEQUENCE_NODE,
    'Bool': VALUE_NODE,
    'Command': UNARY_NODE,
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
    'Define': ASSIGNMENT_NODE,
    'DefineChainProd': ASSIGNMENT_NODE,
    'DefineFn': ASSIGNMENT_NODE,
    'DefineVar': ASSIGNMENT_NODE,
    'DefineVarFn': ASSIGNMENT_NODE,
    'Duration': VALUE_NODE,
    'Float': VALUE_NODE,
    'Flow': SEQUENCE_NODE,
    'FnCall': BINARY_NODE,
    'Get': VALUE_NODE,
    'Ident': VALUE_NODE,
    'Index': BINARY_NODE,
    'Int': VALUE_NODE,
    'List': SEQUENCE_NODE,
    'Literal': VALUE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'Ref': VALUE_NODE,
    'Set': SEQUENCE_NODE,
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'UnaryOp': UNARY_NODE,
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
}


class TreePrint(NodeVisitor):
    def __init__(self):
        super().__init__(_nodeTypeMappings)
        self._ncount = 1
        self._body = []
        self._depth = 0

    def indent(self):
        self._depth += 1

    def dedent(self):
        self._depth -= 1

    def apply(self, tree=None):
        self.visit(tree)
        return self._body

    def format_indent(self):
        return '' if self._depth < 1 else ' '.ljust(self._depth * 4)

    def visit_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1

    # helpers
    def visit_intrinsic(self, value, label=None):
        self._print_object(value, label)
        self._ncount += 1

    def visit_tuple(self, node, label=None):
        self._visit_sequence(node)

    def visit_assignment_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_binary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_sequence(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        if node.value is not None:
            self._visit_sequence(node.values())

    def _visit_sequence(self, li, label=None):
        self.indent()
        if len(li) != 0:
            for n in li:
                if n is not None:
                    self.visit(n)
        self.dedent()

    def visit_unary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.expr)
        self.dedent()

    def visit_value(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1

    def _print_object(self, obj, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        line = '{:5d} : {}{} {}'.format(self._ncount, indent, label, obj)
        self._body.append(line)

    def _print_node(self, node, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
#       op = f' {_._tk2glyph[node.op]}' if isinstance(node, Assign) or isinstance(node, BinOp) else ''
#       op = f' TK.{node.op.name}' if isinstance(node, Assign) else ''
        op = ''
        line = '{:5d} : {}{}{} {}'.format(self._ncount, indent, type(node).__name__, op, node.token.format())
        self._body.append(line)


def print_forest(env, log=None, label=None, print_notation=True, print_results=True):
    idx = 0
    trees = env.trees
    for i in range(0, len(trees)):
        t = trees[i]
        if t is None or t.root is None:
            continue
        idx += 1
        line = env.get_line(t.root.token.location.line).strip()
        ll = f'({label})' if label is not None else ''
        _t_print(log, f'\ntree{idx}:{ll}  {line}')
        print_tree(t, log=log, label=label, print_notation=print_notation, print_results=print_results)


def print_tree(tree, log=None, label=None, print_notation=True, print_results=True):
    printer = FunctionalNotationPrinter()
    if tree is None or tree.root is None:
        return
    print(f'notation: {printer.apply(tree.root)}')
    if tree.values is not None and print_results:
        v = tree.values if type(tree.values).__name__ != 'list' else tree.values[0]
        if getattr(v, 'value', False):
            v = v.value
        ty = type(v).__name__
        if v is None:
            ty = 'Lit'
        _t_print(log, f'result: {ty}({v})')
    print_node(tree.root, log=log, print_notation=False)


def print_node(node, log=None, label=None, print_notation=True):
    printer = FunctionalNotationPrinter()
    if node is None:
        return
    if print_notation:
        print(f'notation: {printer.apply(node)}')
    dt = TreePrint()
    viz = dt.apply(node)
    for v in viz:
        _t_print(log, v)
