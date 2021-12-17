from runtime.environment import Environment
from runtime.stack import RuntimeStack
from runtime.conversion import c_unbox, c_box, c_type
from runtime.exceptions import runtime_error, runtime_strict_warning, getLogFacility
from runtime.literals import Literal
from runtime.token_ids import TK
from runtime.tree import Ref

from runtime.eval_assignment import eval_assign_dispatch, _SUPPORTED_ASSIGNMENT_TOKENS
from runtime.eval_binops import eval_binops_dispatch, _binops_dispatch_table
from runtime.eval_boolean import eval_boolean_dispatch, _boolean_dispatch_table
from runtime.eval_unary import not_literal, increment_literal, decrement_literal, negate_literal, union_literal

_INTRINSIC_VALUE_TYPES = ['bool', 'float', 'int', 'str', 'timedelta']

_INPLACE_OPS = [TK.PLEQ, TK.MNEQ]

_unary2binop = {
    TK.PLEQ: TK.ADD,
    TK.MNEQ: TK.SUB,
}


def get_logger():
    return getLogFacility('focal')


def reduce_value(stack: RuntimeStack, node):
    stack.push(node.value)


def reduce_ref(scope=None, ref=None, value=None, idx=None, update=False):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.define(name=ref.name, value=value, update=update)
    return symbol


def reduce_get(scope=None, get=None):
    scope = Environment.current.scope if scope is None else scope
    if get.tid == TK.ANON:
        symbol = Environment.current.stack.pop()
    else:
        symbol = scope.find(name=get.name)
        if symbol is None:
            runtime_strict_warning(f'Symbol `{get.token.lexeme}` referenced before initialized', loc=get.token.location)
    return symbol


def reduce_propref(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(name=left.name)
    if symbol is None:
        runtime_strict_warning(f'Symbol `{left.token.lexeme}` referenced before initialized', loc=left.token.location)
    prop = symbol.define(right.token.lexeme, local=True)
    return prop


def reduce_propget(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(token=left.token)
    if symbol is None:
        runtime_strict_warning(f'Symbol `{left.token.lexeme}` referenced before initialized', loc=left.token.location)
    prop = symbol.find(right.token.lexeme)
    if prop is None:
        runtime_strict_warning(f'Symbol `{right.token.lexeme}` referenced before initialized', loc=right.token.location)
    return prop


def update_ref(scope=None, name=None, value=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.redefine(name=name, value=value, local=True)
    return symbol


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
        return ref if ref is not None else Literal.NONE(right.token.location)
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


def evaluate_unary_operation(node, l_value):
    opid = node.op
    l_tid = c_type(l_value)
    l_value = c_unbox(l_value)
    if l_value is None:
        return None

    if opid == TK.NOT:
        return not_literal(l_value, l_tid)
    elif opid == TK.INCREMENT:
        l_value = increment_literal(l_value, l_tid)
    elif opid == TK.DECREMENT:
        l_value = decrement_literal(l_value, l_tid)
    elif opid == TK.NEG:
        l_value = negate_literal(l_value, l_tid)
    elif opid == TK.POS:
        pass
    elif opid == TK.ANY:
        l_value = union_literal(l_value, l_tid)
    else:
        runtime_error(f'Invalid operation {opid.name}', loc=None)
    l_value = c_box(l_value, l_value)
    return l_value
