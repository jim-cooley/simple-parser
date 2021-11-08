from environment import Environment
from evaluate import reduce_value, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set, reduce_get, reduce_propref, reduce_ref, update_ref, reduce_parameters
from scope import Block
from visitor import TreeFilter, BINARY_NODE

_VISIT_ASSIGNMENT = 'visit_assignment'
_VISIT_DEFINITION = 'visit_definition'
_VISIT_IDENT = 'visit_ident'
_VISIT_LITERAL = 'visit_literal'
_VISiT_LEAF = 'visit_value'

_PROCESS_APPLY = 'process_apply'
_PROCESS_BINOP = 'process_binop'
_PROCESS_BLOCK = 'process_block'
_PROCESS_DEFINE_FN = 'process_define_fn'
_PROCESS_FLOW = 'process_flow'
_PROCESS_GET = 'process_get'
_PROCESS_PROPREF = 'process_propref'
_PROCESS_REF = 'process_ref'
_PROCESS_SEQUENCE = 'process_sequence_node'
_PROCESS_UNOP = 'process_unop'

_NATIVE_LIST = 'visit_list'
_NATIVE_VALUE = 'process_intrinsic'


_interpreterVisitNodeMappings = {
    'ApplyChainProd': _PROCESS_APPLY,
    'Assign': _VISIT_ASSIGNMENT,
    'BinOp': _PROCESS_BINOP,
    'Block': _PROCESS_BLOCK,
    'Bool': _VISIT_LITERAL,
    'DateDiff': _VISIT_LITERAL,
    'DateTime': _VISIT_LITERAL,
    'Define': _VISIT_DEFINITION,
    'DefineChainProd': _VISIT_DEFINITION,
    'DefineFn': _PROCESS_DEFINE_FN,
    'DefineVar': _VISIT_DEFINITION,
    'DefineVarFn': _PROCESS_DEFINE_FN,
    'Duration': _VISIT_LITERAL,
    'Float': _VISIT_LITERAL,
    'Flow': _PROCESS_FLOW,
    'FnCall': BINARY_NODE,
    'Get': _PROCESS_GET,
    'Ident': _VISIT_IDENT,
    'Index': BINARY_NODE,
    'Int': _VISIT_LITERAL,
    'List': _PROCESS_SEQUENCE,
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

    def __init__(self, environment, mapping=None):
        m = dict(_interpreterVisitNodeMappings if mapping is None else mapping)
        super().__init__(mapping=m, apply_parent_fixups=True)
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
    def process_apply(self, node, label=None):
        self._print_node(node)
        r_value = self.stack.pop()
        self.visit(node.left)
        l_value = self.stack.pop()
        l_value = evaluate_binary_operation(node, l_value, r_value)
        self.stack.push(l_value)

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

    def process_define_fn(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        fn = reduce_ref(ref=left.left)
        fn.code = right
        fn.parameters = reduce_parameters(scope=fn, node=left.right)
#       self.process_binop(node, label)
        self.stack.push(fn)

    def process_flow(self, node, label=None):
        self._print_node(node)
        self.indent()
        values = node.values()
        if values is None:
            self.stack.push(node)
        else:
            prev = None
            for idx in range(0, len(values)):
                n = values[idx]
                if n is None:
                    continue
                if prev is not None:
                    pass  # look for something to assign it to
                self.visit(n)
           #    prev = self.stack.pop()
        self.dedent()

    def process_get(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_get(get=node))

    def process_intrinsic(self, value, lable=None):
        self.stack.push(value)

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

    def process_sequence_node(self, node, label=None):
        self._print_node(node)
        self._process_sequence(node)

    def process_set_object(self, node, label=None):
        self._print_node(node)
        values = node.values()
        if values is None:
            return None
        self.indent()
        evaluate_set(node, self)    # stack items are left on the stack
        self.dedent()

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
