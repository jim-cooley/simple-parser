from environment import Environment
from evaluate import reduce_value, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set, reduce_get, reduce_propref, reduce_ref, update_ref, reduce_parameters
from exceptions import runtime_error
from intrinsic_dispatch import is_intrinsic, invoke_intrinsic
from scope import Block, Object, Scope
from tree import FnCall
from visitor import TreeFilter

_VISIT_IDENT = 'visit_ident'
_VISIT_LITERAL = 'visit_literal'
_VISiT_LEAF = 'visit_value'

_PROCESS_APPLY = 'process_apply'
_PROCESS_ASSIGN = 'process_assignment'
_PROCESS_BINOP = 'process_binop'
_PROCESS_BLOCK = 'process_block'
_PROCESS_DEFINE = 'process_define'
_PROCESS_CHAIN_PROD = 'process_chain_prod'
_PROCESS_DEFINE_FN = 'process_define_fn'
_PROCESS_FLOW = 'process_flow'
_PROCESS_FNCALL = 'process_fncall'
_PROCESS_FNDEF = 'process_fndef'
_PROCESS_GET = 'process_get'
_PROCESS_INDEX = 'process_index'
_PROCESS_LIST = 'process_list_object'
_PROCESS_PROPCALL = 'process_propcall'
_PROCESS_PROPREF = 'process_propref'
_PROCESS_REF = 'process_ref'
_PROCESS_SET = 'process_set_object'
_PROCESS_UNOP = 'process_unop'

_NATIVE_LIST = 'process_native_list'
_NATIVE_VALUE = 'process_native_value'


_interpreterVisitNodeMappings = {
    'ApplyChainProd': _PROCESS_APPLY,
    'Assign': _PROCESS_ASSIGN,
    'BinOp': _PROCESS_BINOP,
    'Block': _PROCESS_BLOCK,
    'Bool': _VISIT_LITERAL,
    'DateDiff': _VISIT_LITERAL,
    'DateTime': _VISIT_LITERAL,
    'Define': _PROCESS_DEFINE,
    'DefineChainProd': _PROCESS_CHAIN_PROD,
    'DefineFn': _PROCESS_DEFINE_FN,
    'DefineVar': _PROCESS_DEFINE,
    'DefineVarFn': _PROCESS_DEFINE_FN,
    'Duration': _VISIT_LITERAL,
    'Float': _VISIT_LITERAL,
    'Flow': _PROCESS_FLOW,
    'FnCall': _PROCESS_FNCALL,
    'FnDef': _PROCESS_FNDEF,
    'Get': _PROCESS_GET,
    'Ident': _VISIT_IDENT,
    'Index': _PROCESS_INDEX,
    'Int': _VISIT_LITERAL,
    'List': _PROCESS_LIST,
    'Literal': _VISIT_LITERAL,
    'Node': _VISiT_LEAF,
    'Percent': _VISIT_LITERAL,
    'PropCall': _PROCESS_PROPCALL,
    'PropRef': _PROCESS_PROPREF,
    'Ref': _PROCESS_REF,
    'Set': _PROCESS_SET,
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

    def visit_literal(self, node, label=None):
        self._print_node(node)
        reduce_value(self.stack, node)

    def visit_value(self, node, label=None):
        self._print_node(node)
        self.stack.push(node)

    def visit_ident(self, node, label=None):
        self._print_node(node)
        self.stack.push(evaluate_identifier(node))

    # -------------------
    # worker nodes
    # -------------------
    # ApplyChainProd
    def process_apply(self, node, label=None):
        self._print_node(node)
        r_value = self.stack.pop()
        self.visit(node.left)
        l_value = self.stack.pop()
        l_value = evaluate_binary_operation(node, l_value, r_value)
        self.stack.push(l_value)

    # Assign
    def process_assignment(self, node, label=None):
        self.process_binop(node, label)

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

    # Block
    def process_block(self, node, label=None):
        self._print_node(node)
        block = Block(loc=node.token.location)
        Environment.enter(block)
        self._process_sequence(node)
        Environment.leave()
        self.stack.push(block)

    # DefineChainProd.  ApplyChainProd is handled via 'Apply'
    def process_chain_prod(self, node, label=None):
        self.process_binop(node, label)

    # Define, DefineVar
    def process_define(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        self.indent()
        self.visit(left)
        self._print_node(right)
        self.dedent()
        # UNDONE: need to handle all cases of ':' operator here as well - or split out
        if isinstance(right, FnCall):
            result = evaluate_invoke(right)
            var = reduce_ref(ref=left, value=result)
        else:
            result = right
            var = reduce_ref(ref=left, value=right)
        var = update_ref(sym=var, value=result)
        self.stack.push(var)

    # DefineFn, DefineVarFn
    def process_define_fn(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        args = node.args
        self.indent()
        self.visit(left)
        self._print_node(args)      # don't visit args on fn def
        self._print_node(right)     # can't visit right w/o executing it
        self.dedent()
        fn = reduce_ref(ref=left)
        if isinstance(right, Scope):
            fn.code = right.items
        else:
            fn.code = right
        fn.defaults = fn.parameters = reduce_parameters(scope=fn, args=args)
        self.stack.push(fn)

    # Flow
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
        self.dedent()

    # FnCall
    def process_fncall(self, node, label=None):
        self._print_node(node)
        self.indent()
        self.visit(node.left)
        self.evaluate_invoke(node)

    # FnDef
    def process_fndef(self, node, label=None):
        self.process_fncall(node, label)

    # Get
    def process_get(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_get(get=node))

    def process_index(self, node, label=None):
        self.process_binop(node, label)

    # encountered if 'tree' is actually a 'forest'
    def process_native_list(self, list, label=None):
        self._print_node(list)
        count = 0
        values = []
        for n in list:
            count += 1
            if self._verbose:
                print(f'\ntree:{count}')
            values.append(self.visit(n))
        self.stack.push(values)

    # int, float, str, ...
    def process_native_value(self, value, lable=None):
        self.stack.push(value)

    # PropCall
    def process_propcall(self, node, label=None):
        self.process_binop(node, label)

    # PropRef
    def process_propref(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        Environment.enter(left)
        self.visit(node.right)
        Environment.leave()
        right = self.stack.pop()
        self.stack.push(reduce_propref(left, right))

    # Ref
    def process_ref(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_ref(ref=node))

    # List
    def process_list_object(self, node, label=None):
        self._print_node(node)
        self._process_sequence(node)

    # Set
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

    def _c_process_sequence(self, seq):
        """
        processes a sequence (list) of items in reverse order (c-style). used by invoke_fn to process arguments.
        """
        self.indent()
        values = seq.values()
        if values is None:
            return seq
        for idx in range(len(values), 0, -1):
            n = values[idx]
            if n is None:
                continue
            self.visit(n)
        self.dedent()

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
        if hasattr(node, 'token'):
            tk = node.token.format()
        else:
            tk = ''
        line = '{}{} {}'.format(type(node).__name__, op, tk)
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

    def evaluate_invoke(self, node):
        fnode = node.left
        args = node.right
        name = fnode.name  # should be either Ref() or Get()
        fn = reduce_get(get=fnode)
        if fn is None:
            runtime_error(f'Function {name} is undefined')
        args = reduce_parameters(scope=fn, args=args)  # need to have scope be a new parameters object (block?)
        if is_intrinsic(name):
            result = invoke_intrinsic(name, args)
            self.stack.push(result)
        else:
            self.invoke_fn(fn, args)

    def invoke_fn(self, fnode, args):
        fnode.update_members(args)
        Environment.enter(fnode)
        self.visit(fnode.code)
        Environment.leave()
