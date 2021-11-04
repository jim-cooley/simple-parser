from environment import Environment
from evaluate import reduce_value, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set, reduce_get, reduce_propref, reduce_ref
from scope import Block
from treeprint import print_node
from visitor import TreeFilter, BINARY_NODE, SEQUENCE_NODE

_VISIT_ASSIGNMENT = 'visit_assignment'
_VISIT_DEFINITION = 'visit_definition'
_VISIT_IDENT = 'visit_ident'
_VISIT_LITERAL = 'visit_literal'
_VISiT_LEAF = 'visit_value'

_PROCESS_BINOP = 'process_binop'
_PROCESS_BLOCK = 'process_block'
_PROCESS_GET = 'process_get'
_PROCESS_PROPREF = 'process_propref'
_PROCESS_REF = 'process_ref'
_PROCESS_UNOP = 'process_unop'

_NATIVE_LIST = 'visit_list'
_NATIVE_VALUE = 'process_intrinsic'


_interpreterVisitNodeMappings = {
    'ApplyChainProd': _VISIT_DEFINITION,
    'Assign': _VISIT_ASSIGNMENT,
    'BinOp': _PROCESS_BINOP,
    'Block': _PROCESS_BLOCK,
    'Bool': _VISIT_LITERAL,
    'Command': 'process_command',
    'DateDiff': _VISIT_LITERAL,
    'DateTime': _VISIT_LITERAL,
    'Define': _VISIT_DEFINITION,
    'DefineChainProd': _VISIT_DEFINITION,
    'DefineFn': _VISIT_DEFINITION,
    'DefineVar': _VISIT_DEFINITION,
    'DefineVarFn': _VISIT_DEFINITION,
    'Duration': _VISIT_LITERAL,
    'Float': _VISIT_LITERAL,
    'Flow': SEQUENCE_NODE,
    'FnCall': BINARY_NODE,
    'Get': _PROCESS_GET,
    'Ident': _VISIT_IDENT,
    'Index': BINARY_NODE,
    'Int': _VISIT_LITERAL,
    'List': SEQUENCE_NODE,
    'Literal': _VISIT_LITERAL,
    'Node': _VISiT_LEAF,
    'Percent': _VISIT_LITERAL,
    'PropCall': BINARY_NODE,
    'PropRef': _PROCESS_PROPREF,
    'Ref': _PROCESS_REF,
    'Set': 'process_set_object',
    'Str': _VISIT_LITERAL,
    'Time': _VISIT_LITERAL,
    'UnaryOp': _PROCESS_UNOP,

    'int': _NATIVE_VALUE,
    'str': _NATIVE_VALUE,
    'list':_NATIVE_LIST,
}


class Interpreter(TreeFilter):

    def __init__(self, environment):
        super().__init__(mapping=_interpreterVisitNodeMappings, apply_parent_fixups=True)
        self.environment = environment
        self.stack = environment.stack
        self._verbose = True

    def apply(self, trees):
        self._init(trees)
        if trees is None:
            return None
        for t in trees:
            self.visit(t.root)
            v = self.stack.pop()
            ty = type(v).__name__
            if getattr(v, 'value', False):
                v = v.value
            t.values = v
            if self._verbose:
                print(f'\nresult: {ty.lower()}({v})\n')
        print(f'stack depth: {self.stack.depth()}')
        return self.trees

    # default
    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        self.stack.push(node.value)

    # encountered if 'tree' is actually a 'forest'
    def visit_list(self, list, label=None):
        self._print_node(list)
        count = 0
        values = []
        for n in list:
            count += 1
            if self._verbose:
                print(f'\ntree:{count}')
            values.append(self.visit(n))
        self.stack.push(values)

    def process_intrinsic(self, value, lable=None):
        self.stack.push(value)

    def visit_literal(self, node, label=None):
        self._print_node(node)
        reduce_value(self.stack, node)

    # node is to be returned (thinks like Ref, etc)
    def visit_value(self, node, label=None):
        self._print_node(node)
        self.stack.push(node)

    # non-converting visitation
    def visit_assignment(self, node, label=None):
        self.process_binop(node, label)

    def visit_definition(self, node, label=None):
        self.process_binop(node, label)

    def visit_ident(self, node, label=None):
        self._print_node(node)
        self.stack.push(evaluate_identifier(node))

    # worker nodes
    def process_binop(self, node, label=None):
        self._print_node(node)
        self.indent()
        self.visit(node.right)
        self.visit(node.left)
        self.dedent()
        l_value = self.stack.pop()
        r_value = self.stack.pop()
        l_value = evaluate_binary_operation(node, l_value, r_value)
        self.stack.push(l_value)

    def process_block(self, node, label=None):
        self._print_node(node)
        block = Block(loc=node.token.location)
        Environment.enter(block)
        self._process_sequence(node)
        Environment.leave()
        self.stack.push(block)

    def process_get(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_get(get=node))

    def process_propref(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        Environment.enter(left)
        self.visit(node.right)
        Environment.leave()
        right = self.stack.pop()
        self.stack.push(reduce_propref(left, right))

    def process_ref(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_ref(ref=node))

    def process_set_object(self, node, label=None):
        self._print_node(node)
        values = node.values()
        if values is None:
            return None
        evaluate_set(node, self)    # stack items are left on the stack

    def process_unop(self, node, label=None):
        self._print_node(node)
        self.indent()
        self.visit(node.expr)
        left = self.stack.pop()
        self.stack.push(evaluate_unary_operation(node, left))

    def _process_sequence(self, seq):
        self.indent()
        values = seq.values()
        if values is None:
            return seq
        for idx in range(0, len(values)):
            n = values[idx]
            if n is None:
                continue
            self.visit(n)
        self.dedent()

    def _init(self, tree):
        self.trees = tree
        self.keywords = self.environment.keywords
        self.globals = self.environment.globals
        self.environment.stack.clear()
        self.stack = self.environment.stack

    def _print_indented(self, message):
        if self._verbose:
            indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
            print(f'{self._count:5d} : {indent}{message}')

    def _print_node(self, node, label=None):
        op = ''
        self._count += 1
        line = '{}{} {}'.format(type(node).__name__, op, node.token.format())
        self._print_indented(line)

    # undone: preserving
    def _print_node2(self, node):
        self._count += 1
        if self._verbose:
            id = ' '
            if getattr(node, 'parent', None) is not None:
                parent = node.parent
                if getattr(parent, '_num', False):
                    id = f'{parent._num + 1}' if parent._num is not None else ' '
            self._print_indented(f'{node}: {node.token.format()}, parent:{id}')
