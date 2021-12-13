from copy import deepcopy

from interpreter.version import VERSION
from runtime.conversion import c_unbox
from runtime.descriptors import ty2descriptor
from runtime.environment import Environment
from runtime.indexdict import IndexedDict
from runtime.literals import Literal
from runtime.options import getOptions
from runtime.scope import Block, Scope, Object, FunctionBase
from runtime.function import Function
from runtime.token import Token
from runtime.tree import Ref, Assign

from runtime.eval_unary import is_true
from runtime.evaluate import reduce_value, evaluate_binary_operation, evaluate_unary_operation, evaluate_identifier, \
    evaluate_set, reduce_get, reduce_propref, reduce_ref, update_ref
from runtime.intrinsics import invoke_generator, tk2generator

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
_PROCESS_COMBINE = 'process_combine'
_PROCESS_DEFINE_FN = 'process_define_fn'
_PROCESS_FLOW = 'process_flow'
_PROCESS_FNCALL = 'process_fncall'
_PROCESS_FNREF = 'process_fnref'
_PROCESS_GENERATOR = 'process_generator'
_PROCESS_GET = 'process_get'
_PROCESS_CONDITIONAL = 'process_conditional'
_PROCESS_INDEX = 'process_index'
_PROCESS_INDEX_SET = 'process_index_set'
_PROCESS_LIST = 'process_list_object'
_PROCESS_PROPCALL = 'process_propcall'
_PROCESS_PROPREF = 'process_propref'
_PROCESS_PROPSET = 'process_propset'
_PROCESS_REF = 'process_ref'
_PROCESS_SET = 'process_set_object'
_PROCESS_SLICE = 'process_slice'
_PROCESS_UNOP = 'process_unop'

_NATIVE_LIST = 'process_native_list'
_NATIVE_VALUE = 'process_native_value'


_interpreterVisitNodeMappings = {
    'ApplyChainProd': _PROCESS_APPLY,
    'Assign': _PROCESS_ASSIGN,
    'BinOp': _PROCESS_BINOP,
    'Block': _PROCESS_BLOCK,
    'Bool': _VISIT_LITERAL,
    'Category': _VISIT_LITERAL,
    'Combine': _PROCESS_COMBINE,
    'DateDiff': _VISIT_LITERAL,
    'DateTime': _VISIT_LITERAL,
    'Define': _PROCESS_DEFINE,
    'DefineChainProd': _PROCESS_CHAIN_PROD,
    'DefineFn': _PROCESS_DEFINE_FN,
    'DefineVal': _PROCESS_DEFINE,
    'DefineVar': _PROCESS_DEFINE,
    'DefineValFn': _PROCESS_DEFINE_FN,
    'DefineVarFn': _PROCESS_DEFINE_FN,
    'Dict': _PROCESS_SET,
    'Duration': _VISIT_LITERAL,
    'Enumeration': _VISIT_LITERAL,
    'Float': _VISIT_LITERAL,
    'Flow': _PROCESS_FLOW,
    'FnCall': _PROCESS_FNCALL,
    'FnRef': _PROCESS_FNREF,
    'Generate': _PROCESS_GENERATOR,
    'GenerateRange': _PROCESS_GENERATOR,
    'Get': _PROCESS_GET,
    'Ident': _VISIT_IDENT,
    'IfThenElse': _PROCESS_CONDITIONAL,
    'Index': _PROCESS_INDEX,
    'IndexSet': _PROCESS_INDEX_SET,
    'Int': _VISIT_LITERAL,
    'List': _PROCESS_LIST,
    'Literal': _VISIT_LITERAL,
    'NamedTuple': _PROCESS_SET,
    'Node': _VISiT_LEAF,
    'Percent': _VISIT_LITERAL,
    'PropCall': _PROCESS_PROPCALL,
    'PropRef': _PROCESS_PROPREF,
    'PropSet': _PROCESS_PROPSET,
    'Ref': _PROCESS_REF,
    'Return': _UNBOX_EXPR,
    'Set': _PROCESS_SET,
    'Slice': _PROCESS_SLICE,
    'Str': _VISIT_LITERAL,
    'Time': _VISIT_LITERAL,
    'Tuple': _PROCESS_LIST,
    'UnaryOp': _PROCESS_UNOP,

    'int': _NATIVE_VALUE,
    'str': _NATIVE_VALUE,
    'list': _NATIVE_LIST,
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
            v = self.visit(t.root)
            if v is None:
                v = self.stack.peek()
            t.values = v
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
        value = self._process_sequence(node)    # UNDONE: likely don't want to evaluate the block, just push it.
        Environment.leave()
        if value is not None:
            self.stack.push(value[-1])
        else:
            self.stack.push(None)

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

    # Combine
    def process_combine(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        self.indent()
        self.visit(left)
        l_val = self.stack.pop()
        self.visit(right)
        r_val = self.stack.pop()
        if isinstance(left, Ref):
            var = reduce_ref(ref=left, value=r_val)
            self.stack.push(var)
        else:
            self.stack.push((l_val, r_val))

    # Define, DefineVar
    def process_define(self, node, label=None):
        self._print_node(node)
        left = node.left
        right = node.right
        self.indent()
        self.visit(left)
        if not isinstance(right, Block):
            self.visit(right)
            result = self.stack.pop()
        else:
            self._print_node(right)
            result = right
        self.dedent()
        var = reduce_ref(ref=left, value=result, update=True)
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
        if not isinstance(fn, Function):
            fn = Function(other=fn, closure=Environment.current.scope)
            if isinstance(right, Scope):
                fn.from_block(right, copy=False)
            else:
                fn.code = right
            fn.defaults = fn.parameters = self.reduce_parameters(scope=fn, args=args)
            update_ref(name=fn.name, value=fn)
        self.stack.push(fn)

    # Flow
    def process_flow(self, node, label=None):
        self._print_node(node)
        self.indent()
        values = node.values()
        if values is None:
            self.stack.push(node)
        else:
            for idx in range(0, len(values)):
                n = values[idx]
                if n is None:
                    continue
                if isinstance(n, Ref):
                    symbol = Environment.current.scope.find(name=n.name)
                    if symbol is not None:
                        if isinstance(symbol, FunctionBase):
                            self.evaluate_invoke(n.name, symbol)
                        else:
                            self.stack.push(symbol)
                    else:
                        result = self.stack.pop()
                        var = reduce_ref(ref=n, value=result, update=True)
                        self.stack.push(var)
                else:
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
        args = self.reduce_parameters(scope=None, args=node.items())  # process & return them as an IndexedDict
        fname = tk2generator[node.target]
        result = invoke_generator(name=fname, args=args)
        self.dedent()
        self.stack.push(result)

    # Get
    def process_get(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_get(get=node))

    def process_index(self, node, label=None):
        self.process_binop(node, label)

    def process_index_set(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        if hasattr(left, 'value'):
            left = left.value
        self.visit(node.value)
        value = self.stack.pop()
        self.visit(node.index)
        index = self.stack.pop()
        if hasattr(index, 'value'):
            index = index.value
        desc = ty2descriptor(left)
        if desc is not None:
            if node.right is None:
                desc.setAt(left, None, index, value)
            elif isinstance(node.right, Ref):
                desc.setAt(left, node.right.name, index, value)
            return
        # invalid?
        Environment.enter(left)
        self.visit(node.right)
        Environment.leave()

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
        self._print_node(node)
        self.indent()
        self.visit(node.left)
        obj = self.stack.pop()
        args = node.right
        if hasattr(obj, 'value'):
            obj = obj.value
        desc = ty2descriptor(obj)
        if desc is not None:
            method = node.member.name
            args = self.reduce_parameters(fn=None, scope=None, args=args)
            result = desc.invoke(obj, method, args)
            self.stack.push(result)
            return

    # PropRef
    def process_propref(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        if hasattr(left, 'value'):
            left = left.value
        desc = ty2descriptor(left)
        if desc is not None:
            if isinstance(node.right, Ref):
                result = desc.get(left, node.right.name)
                self.stack.push(result)
                return
        Environment.enter(left)
        self.visit(node.right)
        Environment.leave()

    # PropSet
    def process_propset(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        self.visit(node.value)
        value = self.stack.pop()
        if hasattr(left, 'value'):
            left = left.value
        desc = ty2descriptor(left)
        if desc is not None:
            if isinstance(node.right, Ref):
                desc.set(left, node.right.name, value)
                return
        # invalid?
        Environment.enter(left)
        self.visit(node.right)
        Environment.leave()

    # Ref
    def process_ref(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_ref(ref=node))

    # List
    def process_list_object(self, node, label=None):
        self._print_node(node)
        node.set_values(self._process_sequence(node))
        self.stack.push(node)

    # Set
    def process_set_object(self, node, label=None):
        self._print_node(node)
        values = node.values()
        if values is None:
            return None
        self.indent()
        evaluate_set(node, self)    # stack items are left on the stack
        self.dedent()

    def process_slice(self, node, label=None):
        self._print_node(node)
        self.indent()
        start = end = step = None
        if node.start is not None:
            self.visit(node.start)
            start = self.stack.pop()
        if node.end is not None:
            self.visit(node.end)
            end = self.stack.pop()
        if node.step is not None:
            self.visit(node.step)
            step = self.stack.pop()
        self.dedent()
        self.stack.push([start, end, step])

    def process_unop(self, node, label=None):
        self._print_node(node)
        self.indent()
        self.visit(node.expr)
        left = self.stack.pop()
        self.stack.push(evaluate_unary_operation(node, left))

    # these need access to stack:
    def evaluate_invoke(self, name, fnode, args=None):
        assert fnode is not None, f'Function {name} is undefined'
        args = self.reduce_parameters(fn=fnode, args=args)
        result = fnode.invoke(self, args)
        self.stack.push(result)

    def reduce_parameters(self, scope=None, fn=None, args=None):
        _values = []
        _fields = []
        _defaults = {}
        if scope is not None:
            Environment.enter(scope)
        if fn is None:
            fn = scope
        if hasattr(fn, 'defaults'):
            if fn.defaults is not None:
                _defaults = deepcopy(fn.defaults)
                _fields = list(_defaults.keys())
                _values = list(_defaults.values())
        if args is not None:
            for idx in range(0, len(args)):
                ref = args[idx]
                if isinstance(ref, Assign):
                    self.visit(ref.right)
                    value = self.stack.pop()
                    sym = reduce_ref(scope=scope, ref=ref.left)
                    if isinstance(sym, Object):
                        name = sym.name
                    elif isinstance(sym, Token):    # tokens are keywords / intrinsics
                        name = sym.lexeme
                    else:
                        assert False, "Unexpected argument type in Define"
                    self._resolve(idx, name, c_unbox(value), _fields, _values)
                else:
                    if isinstance(ref, Literal) or ref is None:
                        self._resolve(idx, None, c_unbox(ref), _fields, _values)
                    else:
                        self.visit(ref)
                        val = self.stack.pop()
                        if isinstance(ref, Ref):
                            name = ref.name
                        else:
                            name = None
                        self._resolve(idx, name, c_unbox(val), _fields, _values)
        else:
            for idx in range(0, fn.arity):
                val = self.stack.pop()
                self._resolve(idx, None, c_unbox(val), _fields, _values)
        if scope is not None:
            Environment.leave()
        return IndexedDict(fields=_fields, values=_values)

    def _resolve(self, idx, name, value, fields, values):
        if name is None:
            if idx < len(values):
                values[idx] = value
            else:
                values.append(value)
                if idx >= len(fields):
                    fields.append(None)
        else:
            if name in fields:
                slot = fields.index(name)
                values[slot] = value
            else:
                fields.append(name)
                values.append(value)

    def _process_sequence(self, seq):
        self.indent()
        items = seq.items()  # was values()
        values = []
        if items is None:
            return seq
        for idx in range(0, len(items)):
            n = items[idx]
            if n is None:
                continue
            self.visit(n)
            values.append(self.stack.pop())
        self.dedent()
        return values

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
