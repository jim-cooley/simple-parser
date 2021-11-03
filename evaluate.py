from environment import Environment
from eval_binops import eval_binops_dispatch, _binops_dispatch_table
from eval_unary import not_literal, increment_literal, decrement_literal, negate_literal
from literals import LIT_NONE
from tokens import TK, TCL

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'timedelta']
_INTRINSIC_STR_TYPE = 'str'

_INPLACE_OPS = [TK.PLEQ, TK.MNEQ]

_unary2binop = {
    TK.PLEQ:    TK.ADD,
    TK.MNEQ:    TK.SUB,
}


def get_logger():
    return Environment.current.logger


def evaluate_literal(node):
    return node.value


def evaluate_identifier(node):
    left = Environment.current.symbols.find(node.token)
    return left


def evaluate_binary_operation(node, left, right):
    op = node.op
    if op in _binops_dispatch_table:
        return eval_binops_dispatch(node, left, right)
    elif op == TK.DEF:
        scope = Environment.current.symbols
        symbol = scope.find_add(left.token)
        scope = Environment.current.enter_scope(symbol)
        ref = scope.find_add_local(right.token)
        Environment.current.leave_scope(scope)
        return ref if ref is not None else LIT_NONE
    else:
        get_logger().error(f'Invalid operation {op.id.name}', loc=op.location)
    return None  # fixups uses this code as well.  probably want option_strict enablement
    """
    elif op == TK.REF:
        scope = Environment.current.symbols
        symbol = scope.find(left.token)
        if symbol is None:
            return LIT_NONE
        scope = Environment.current.enter_scope(symbol)
        ref = scope.find_local(right.token)
        Environment.current.leave_scope(scope)
        if ref is None:
            return LIT_NONE
        return ref.value if ref is not None else LIT_NONE
    elif op == TK.ASSIGN:
        scope = Environment.current.symbols
        token = left.token
        if isinstance(left.value, AST):
            token = left.value.token
            scope = left.value.parent_scope
        symbol = scope.find_add_local(token, right.value)
        symbol.value = right.value
        return right.value
    elif op in _INPLACE_OPS:
        left = Environment.current.symbols.find(left.token)
        if left is not None:
            op = _unary2binop[op]
            left.value = eval_binops_dispatch2(op, left.value, right.value)
            return left.value
        get_logger().runtime_error(
            f'Variable ({left.token.lexeme}) used before being initialized', loc=left.token.location)
    """


def evaluate_set(node, visitor=None):
    if node is None:
        return None
    values = node.values()
    if values is None:
        return None
    scope = Environment.current.enter_scope(node)
    node.value = scope
    for idx in range(0, len(values)):
        n = values[idx]
        if n is None:
            continue
        visitor.visit(n)
    Environment.current.leave_scope(scope)
    return node


def evaluate_unary_operation(node, expr):
    tid = node.op
    left = node.expr

    if left.token.value is None:
        return None

    if left.token.t_class == TCL.LITERAL:
        if tid == TK.NOT:
            return not_literal(left).value
        elif tid == TK.INCREMENT:
            return increment_literal(left).value
        elif tid == TK.DECREMENT:
            return decrement_literal(left).value
        elif tid == TK.NEG:
            return negate_literal(left).value
        elif tid == TK.POS:
            return left.value
    return node.value
