from environment import Environment
from eval_binops import eval_binops_dispatch, _binops_dispatch_table, eval_binops_dispatch2
from eval_unary import not_literal, increment_literal, decrement_literal, negate_literal
from exceptions import _runtime_error, _error
from tokens import TK, TCL

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'timedelta']
_INTRINSIC_STR_TYPE = 'str'

_INPLACE_OPS = [TK.PLEQ, TK.MNEQ]

_unary2binop = {
    TK.PLEQ:    TK.ADD,
    TK.MNEQ:    TK.SUB,
}


def evaluate_literal(node):
    return node.value


def evaluate_identifier(node):
    left = Environment.current.symbols.find(node.token)
    if left is None:
        return None
    return left.value


def evaluate_binary_operation(node):
    op = node.op
    if op in _binops_dispatch_table:
        return eval_binops_dispatch(node)
    elif op == TK.ASSIGN:
        scope = Environment.current.symbols
        symbol = scope.find_add_local(node.left.token, node.right.value)
        symbol.value = node.right.value
        return node.right.value
    elif op in _INPLACE_OPS:
        left = Environment.current.symbols.find(node.left.token)
        if left is not None:
            op = _unary2binop[op]
            left.value = eval_binops_dispatch2(op, left.value, node.right.value)
            return left.value
        _runtime_error(f'Variable ({node.left.token.lexeme}) used before being initialized', loc=node.token.location)
    return None  # fixups uses this code as well.  probably want option_strict enablement
    _error(f'Invalid operation {node.token.id.name}', loc=node.token.location)


def evaluate_unary_operation(node):
    tid = node.op
    left = node.expr

    if left.token.value is None:
        return None

    if left.token.t_class == TCL.LITERAL:
        if tid == TK.NOT:
            return not_literal(left)
        elif tid == TK.INCREMENT:
            return increment_literal(left)
        elif tid == TK.DECREMENT:
            return decrement_literal(left)
        elif tid == TK.NEG:
            return negate_literal(left)
        elif tid == TK.POS:
            return left
    return node