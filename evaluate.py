from copy import deepcopy

from conversion import c_unbox, c_box
from environment import Environment, RuntimeStack
from eval_assignment import eval_assign_dispatch, _SUPPORTED_ASSIGNMENT_TOKENS
from eval_binops import eval_binops_dispatch, _binops_dispatch_table
from eval_boolean import eval_boolean_dispatch, _boolean_dispatch_table
from eval_unary import not_literal, increment_literal, decrement_literal, negate_literal
from exceptions import runtime_error, runtime_strict_warning, getLogFacility
from indexed_dict import IndexedDict
from intrinsic_dispatch import invoke_fn, is_intrinsic, invoke_intrinsic
from literals import LIT_NONE, Literal
from tokens import TK
from tree import Ref, Define

_INTRINSIC_VALUE_TYPES = ['bool', 'float', 'int', 'str', 'timedelta']

_INPLACE_OPS = [TK.PLEQ, TK.MNEQ]

_unary2binop = {
    TK.PLEQ: TK.ADD,
    TK.MNEQ: TK.SUB,
}


def get_logger():
    return getLogFacility('semtex')


def reduce_value(stack: RuntimeStack, node):
    stack.push(node.value)


def reduce_ref(scope=None, ref=None, value=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.define(ref.token.lexeme, value)
    # UNDONE: need to update definitions if symbol exists.  need to call assignment, not update_ref
    return symbol  # should be Object type


def reduce_get(scope=None, get=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.find(get.token.lexeme)
    if symbol is None:
        runtime_strict_warning(f'Symbol `{get.token.lexeme}` referenced before initialized', loc=get.token.location)
    return symbol


def reduce_propref(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(left.token.lexeme)
    if symbol is None:
        runtime_strict_warning(f'Symbol `{left.token.lexeme}` referenced before initialized', loc=left.token.location)
    prop = symbol.define(right.token.lexeme, local=True)
    return prop


def reduce_propget(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(left.token.lexeme)
    if symbol is None:
        runtime_strict_warning(f'Symbol `{left.token.lexeme}` referenced before initialized', loc=left.token.location)
    prop = symbol.find(right.token.lexeme)
    if prop is None:
        runtime_strict_warning(f'Symbol `{right.token.lexeme}` referenced before initialized', loc=right.token.location)
    return prop


def reduce_parameters(scope=None, args=None):
    items = {}
    if scope is not None:
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
                items[sym.name] = value
            elif isinstance(ref, Ref):
                sym = reduce_ref(scope=scope, ref=ref)
                items[sym.name] = sym
            elif isinstance(ref, Literal):
                slot = items.keys()[idx]
                items[slot] = c_unbox(ref),
    return IndexedDict(items)


def update_ref(scope=None, sym=None, value=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.update(sym.name, value, local=True)
    return symbol  # should be Object type


def evaluate_binary_operation(node, left, right):
    op = node.op
    if isinstance(left, Ref):
        left = reduce_ref(scope=Environment.current.scope, ref=left)
    if isinstance(right, Ref):
        right = reduce_ref(scope=Environment.current.scope, ref=right)
    if op in _binops_dispatch_table:
        return eval_binops_dispatch(node, left, right)
    elif op in _boolean_dispatch_table:
        return eval_boolean_dispatch(node, left, right)
    elif op in [TK.DEF, TK.REF]:
        scope = Environment.current.scope
        symbol = scope.define(left.token.lexeme)
        ref = symbol.define(right.token.lexeme, local=True)
        return ref if ref is not None else LIT_NONE
    elif op in [TK.ASSIGN, TK.DEFINE, TK.APPLY]:
        if op in _SUPPORTED_ASSIGNMENT_TOKENS:
            return eval_assign_dispatch(node, left, right)
        else:
            runtime_error(f'Type mismatch for assignment({type(left)}, {type(right)})', loc=None)
    else:
        get_logger().error(f'Invalid operation {op.name}', loc=node.token.location)
    return None  # fixups uses this code as well.  probably want option_strict enablement


def evaluate_identifier(stack, node):
    left = Environment.current.scope.find(node.token.lexeme)
    stack.push(left)


def evaluate_invoke(node):
    fnode = node.left
    args = node.right
    name = fnode.name  # should be either Ref() or Get()
    fn = reduce_get(get=fnode)
    if fn is None:
        runtime_error(f'Function {name} is undefined')
    args = reduce_parameters(scope=fn, args=args)  # need to have scope be a new parameters object (block?)
    if is_intrinsic(name):
        result = invoke_intrinsic(name, args)
    else:
        ident = reduce_get(get=node.left)
        result = invoke_fn(ident, args)
    return result


def evaluate_set(node, visitor=None):
    if node is None:
        return None
    values = node.values()
    if values is None:
        return None
    scope = Environment.enter(node)
    node.value = scope
    for idx in range(0, len(values)):
        n = values[idx]
        if n is None:
            continue
        visitor.visit(n)
    Environment.leave()
    return node


def evaluate_unary_operation(node, left):
    opid = node.op
    l_tid = TK.NATIVE
    if getattr(left, 'token', False):
        l_tid = left.token.id
    l_value = c_unbox(left)

    if l_value is None:
        return None

    if opid == TK.NOT:
        return not_literal(l_value, l_tid)
    elif opid == TK.INCREMENT:
        l_value = increment_literal(l_value, l_tid)
    #        eval_assign_dispatch(left, r_value),
    elif opid == TK.DECREMENT:
        l_value = decrement_literal(l_value, l_tid)
    #        eval_assign_dispatch(left, r_value),
    elif opid == TK.NEG:
        l_value = negate_literal(l_value, l_tid)
    #        eval_assign_dispatch(left, r_value),
    elif opid == TK.POS:
        pass
    else:
        runtime_error(f'Invalid operation {opid.name}', loc=None)

    left = c_box(left, l_value)
    return left
