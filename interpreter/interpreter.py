from copy import deepcopy

from interpreter.version import VERSION
from runtime.conversion import c_unbox
from runtime.environment import Environment
from runtime.exceptions import runtime_error
from runtime.indexdict import IndexedDict
from runtime.literals import Literal
from runtime.options import getOptions
from runtime.scope import Block, Scope, Object
from runtime.token import Token
from runtime.tree import FnCall, Define, Ref, Generate

from runtime.eval_unary import is_true
from runtime.evaluate import reduce_value, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set, reduce_get, reduce_propref, reduce_ref, update_ref
from runtime.dispatch import is_intrinsic, invoke_intrinsic, invoke_generator, tk2generator

from interpreter.visitor import TreeFilter


_VISIT_IDENT = 'visit_ident'
_VISIT_LITERAL = 'visit_literal'
_VISiT_LEAF = 'visit_value'
_UNBOX_NODE = 'unbox_node'
_UNBOX_EXPR = 'unbox_expression'

_PROCESS_APPLY = 'process_apply'
_PROCESS_ASSIGN = 'process_assignment'
_PROCESS_BINOP = 'process_binop'
_PROCESS_BLOCK = 'process_block'
_PROCESS_DEFINE = 'process_define'
_PROCESS_CHAIN_PROD = 'process_chain_prod'
_PROCESS_DEFINE_FN = 'process_define_fn'
_PROCESS_FLOW = 'process_flow'
_PROCESS_FNCALL = 'process_fncall'
_PROCESS_FNREF = 'process_fnref'
_PROCESS_GENERATOR = 'process_generator'
_PROCESS_GET = 'process_get'
_PROCESS_CONDITIONAL = 'process_conditional'
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
    'FnRef': _PROCESS_FNREF,
    'Generate': _PROCESS_GENERATOR,
    'Get': _PROCESS_GET,
    'Ident': _VISIT_IDENT,
    'IfThenElse': _PROCESS_CONDITIONAL,
    'Index': _PROCESS_INDEX,
    'Int': _VISIT_LITERAL,
    'List': _PROCESS_LIST,
    'Literal': _VISIT_LITERAL,
    'Node': _VISiT_LEAF,
    'Percent': _VISIT_LITERAL,
    'PropCall': _PROCESS_PROPCALL,
    'PropRef': _PROCESS_PROPREF,
    'Ref': _PROCESS_REF,
    'Return': _UNBOX_EXPR,
    'Set': _PROCESS_SET,
    'Str': _VISIT_LITERAL,
    'Time': _VISIT_LITERAL,
    'UnaryOp': _PROCESS_UNOP,

    'int': _NATIVE_VALUE,
    'str': _NATIVE_VALUE,
    'list':_NATIVE_LIST,
}


class Interpreter(TreeFilter):

    def __init__(self, mapping=None):
        m = dict(_interpreterVisitNodeMappings if mapping is None else mapping)
        super().__init__(mapping=m, apply_parent_fixups=True)
        self.stack = None
        self.option = getOptions('focal')
        self.version = VERSION

    def apply(self, environment=None):
        self._init(environment)
        if environment is None:
            return None
        assert environment.trees is not None, "empty trees passed via Environment to apply"

        for t in environment.trees:
            self.visit(t.root)
            v = self.stack.pop()
            ty = type(v).__name__
            if hasattr(v, 'value'):
                v = v.value
            t.values = v
            if self.option.verbose:
                print(f'\nresult: {ty.lower()}({v})\n')
        if self.option.verbose:
            print(f'stack depth: {self.stack.depth()}')
        return environment

    # default
    def visit_node(self, node, label=None):
        self.unbox_node(node, label)

    def visit_literal(self, node, label=None):
        self._print_node(node)
        reduce_value(self.stack, node)

    def visit_value(self, node, label=None):
        self._print_node(node)
        self.stack.push(node)

    def visit_ident(self, node, label=None):
        self._print_node(node)
        self.stack.push(evaluate_identifier(node))

    def unbox_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        self.stack.push(node.value)

    def unbox_expression(self, node, label=None):
        self._print_node(node)
        self.visit(node.expr)

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

    def process_conditional(self, node, label=None):
        self._print_node(node)
        test = node.test
        then = node.then
        els = node.els
        self.indent()
        self.visit(test)
        result = is_true(c_unbox(self.stack.pop()), tid=None)
        if result:
            self.visit(then)
        else:
            self.visit(els)

    # Define, DefineVar
    def process_define(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        self.indent()
        self.visit(left)
        # UNDONE: need to handle all cases of ':' operator here as well - or split out
        if isinstance(right, FnCall) or isinstance(right, Generate):
            self.visit(right)
            result = self.stack.pop()
            var = reduce_ref(ref=left, value=result)
        else:
            self._print_node(right)
            result = right
            var = reduce_ref(ref=left, value=right)
        self.dedent()
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
        self._print_node(args)      # don't visit args on fn def. UNDONE: scan for anything but ident, or ident=value
        self._print_node(right)     # can't visit right w/o executing it
        self.dedent()
        fn = self.stack.pop()
        if isinstance(right, Scope):
            fn.from_block(right)
        else:
            fn.code = right
        fn.defaults = fn.parameters = self.reduce_parameters(scope=fn, args=args)
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
        fnode = self.stack.pop()
        args = node.right
        self.evaluate_invoke(node.left.name, fnode, args)

    # FnDef
    def process_fnref(self, node, label=None):
        self.process_fncall(node, label)

    # Generator
    def process_generator(self, node, label=None):
        self._print_node(node)
        self.indent()
        # self._process_sequence(node)  # this will process and push the parameters to the stack.
        args = self.reduce_parameters(scope=None, args=node.items())  # process & return them as an IndexedDict
        fname = tk2generator[node.target]
        result = invoke_generator(env=self.environment, name=fname, args=args)
        self.dedent()
        self.stack.push(result)

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
            if self.option.verbose:
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

    # these need access to stack:
    def evaluate_invoke(self, name, fn, args):
        if fn is None:
            runtime_error(f'Function {name} is undefined')
        args = self.reduce_parameters(scope=fn, args=args)  # need to have scope be a new parameters object (block?)
        if is_intrinsic(name):
            result = invoke_intrinsic(env=self.environment, name=name, args=args)
            self.stack.push(result)
        else:
            self.invoke_fn(fn, args)

    def invoke_fn(self, fnode, args):
        fnode.update_members(args)
        Environment.enter(fnode)
        self.visit(fnode.code)
        Environment.leave()

    # VERIFY: this may not handle embedded expressions correctly
    # the reason that this is not simply _process_sequence is that it must handle k:v pairs without evaluating them
    def reduce_parameters(self, scope=None, args=None):
        items = {}
        if scope is not None:
            Environment.enter(scope)
            if hasattr(scope, 'defaults'):
                if scope.defaults is not None:
                    items = deepcopy(scope.defaults)
        if args is not None:
            for idx in range(0, len(args)):
                ref = args[idx]
                if isinstance(ref, Define):
                    value = ref.right
                    ref = ref.left
                    sym = reduce_ref(scope=scope, ref=ref)
                    if isinstance(sym, Object):
                        items[sym.name] = value
                    elif isinstance(sym, Token):    # tokens are keywords / reserved words
                        items[sym.lexeme] = value
                    else:
                        slot = list(items.keys())[idx]
                        items[slot] = c_unbox(sym)
                elif isinstance(ref, Ref):
                    sym = reduce_ref(scope=scope, ref=ref)
                    if isinstance(sym, Object):
                        items[sym.name] = sym
                    else:
                        slot = list(items.keys())[idx]
                        items[slot] = c_unbox(sym)
                elif isinstance(ref, Literal):
                    if idx >= len(items):
                        v = c_unbox(ref)
                        items[v] = v
                    else:
                        slot = list(items.keys())[idx]
                        items[slot] = c_unbox(ref)
                else:
                    self.visit(ref)
                    val = self.stack.pop()
                    slot = list(items.keys())[idx]
                    items[slot] = c_unbox(val)  # UNDONE: is this legit on named parameters?
        if scope is not None:
            Environment.leave()
        return IndexedDict(items)

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

    def _init(self, environment):
        Environment.current = environment
        self.environment = environment
        self.keywords = self.environment.keywords
        self.globals = self.environment.globals
        self.stack = self.environment.stack

    def _print_indented(self, message):
        if self.option.verbose:
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
        if self.option.verbose:
            id = ' '
            if hasattr(node, 'parent'):
                parent = node.parent
                if hasattr(parent, '_num'):
                    id = f'{parent._num + 1}' if parent._num is not None else ' '
            self._print_indented(f'{node}: {node.token.format()}, parent:{id}')
