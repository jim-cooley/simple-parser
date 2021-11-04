from conversion import c_unbox, c_box
from environment import Environment, RuntimeStack
from eval_assignment import eval_assignment_dispatch, _SUPPORTED_ASSIGNMENT_TOKENS
from eval_binops import eval_binops_dispatch, _binops_dispatch_table
from eval_unary import not_literal, increment_literal, decrement_literal, negate_literal
from literals import LIT_NONE
from tokens import TK, TCL
from tree import Ref

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'timedelta']
_INTRINSIC_STR_TYPE = 'str'

_INPLACE_OPS = [TK.PLEQ, TK.MNEQ]

_unary2binop = {
    TK.PLEQ:    TK.ADD,
    TK.MNEQ:    TK.SUB,
}


def get_logger():
    return Environment.current.logger


def reduce_value(stack: RuntimeStack, node):
    stack.push(node.value)


def reduce_ref(scope=None, ref=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.find_add_local(ref.token)
    return symbol   # should be Object type


def reduce_get(scope=None, get=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = scope.find(get.token)
    if symbol is None:
        Environment.get_logger().runtime_error(f'Symbol `{get.token.lexeme}` does not exist', loc=get.token.location)
    return symbol


def reduce_propref(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(left.token)
    if symbol is None:
        Environment.get_logger().runtime_error(f'Symbol `{left.token.lexeme}` does not exist', loc=left.token.location)
    prop = symbol.find_add_local(right.token)
    return prop


def reduce_propget(left=None, right=None):
    scope = Environment.current.scope
    symbol = scope.find(left.token)
    if symbol is None:
        Environment.get_logger().runtime_error(f'Symbol `{left.token.lexeme}` does not exist', loc=left.token.location)
    prop = symbol.find(right.token)
    if prop is None:
        Environment.get_logger().runtime_error(f'Symbol `{right.token.lexeme}` does not exist', loc=right.token.location)
    return prop


def evaluate_identifier(stack, node):
    left = Environment.current.scope.find(node.token)
    stack.push(left)


def evaluate_binary_operation(node, left, right):
    op = node.op
    if isinstance(left, Ref):
        left = reduce_ref(scope=Environment.current.scope, ref=left)
    if isinstance(right, Ref):
        right = reduce_ref(scope=Environment.current.scope, ref=right)
    if op in _binops_dispatch_table:
        return eval_binops_dispatch(node, left, right)
    elif op in [TK.DEF, TK.REF]:
        scope = Environment.current.scope
        symbol = scope.find_add(left.token)
        ref = symbol.find_add_local(right.token)
        return ref if ref is not None else LIT_NONE
    elif op in [TK.ASSIGN, TK.DEFINE]:
        if op in _SUPPORTED_ASSIGNMENT_TOKENS:
            return eval_assignment_dispatch(left, right)
        else:
            get_logger().runtime_error(f'Type mismatch for assignment({type(left)}, {type(right)})', loc=None)
#        left.value = right
#        return left  # UNDONE: return the object or its value?
    else:
        get_logger().error(f'Invalid operation {op.name}', loc=node.token.location)
    return None  # fixups uses this code as well.  probably want option_strict enablement


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
#        eval_assignment_dispatch(left, r_value),
    elif opid == TK.DECREMENT:
        l_value = decrement_literal(l_value, l_tid)
#        eval_assignment_dispatch(left, r_value),
    elif opid == TK.NEG:
        l_value = negate_literal(l_value, l_tid)
#        eval_assignment_dispatch(left, r_value),
    elif opid == TK.POS:
        pass
    else:
        get_logger().error(f'Invalid operation {opid.name}', loc=None)

    left = c_box(left, l_value)
    return left
