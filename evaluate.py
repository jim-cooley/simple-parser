from eval_binops import eval_binops_dispatch
from eval_unary import not_literal, increment_literal, decrement_literal, negate_literal
from exceptions import _runtime_error
from tokens import TK, TCL

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'timedelta']
_INTRINSIC_STR_TYPE = 'str'


def evaluate_literal(node):
    return node.value


def evaluate_binary_operation(node):
    return eval_binops_dispatch(node)


def evaluate_binary_operation2(node):
    token = node.token
    tid = token.id
    l_value = node.left.value
    l_ty = type(l_value).__name__
    r_value = node.right.value
    r_ty = type(r_value).__name__

    # UNDONE: need dynamic dispatch here
    if l_value is None or r_value is None:
        return None

    if l_ty not in _INTRINSIC_VALUE_TYPES or r_ty not in _INTRINSIC_VALUE_TYPES:
        return None

    if tid == TK.ADD:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value + r_value
                return node
            elif r_ty == _INTRINSIC_STR_TYPE:
                node.value = f'{l_value}' + r_value
                return node
        elif l_ty == _INTRINSIC_STR_TYPE:
            if r_ty == _INTRINSIC_STR_TYPE:
                node.value = l_value + r_value
                return node
            else:
                node.value = l_value + f'{r_value}'
                return node
        _runtime_error(f"Type mismatch for operator.__add__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.SUB:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value - r_value
                return node
        _runtime_error(f"Type mismatch for operator.__sub__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.MUL:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value * r_value
                return node
            elif r_ty == _INTRINSIC_STR_TYPE:
                node.value = l_value + r_value
                return node
        elif l_ty == _INTRINSIC_STR_TYPE:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value * r_value
                return node
        _runtime_error(f"Type mismatch for operator.__mul__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.DIV:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value / r_value
                return node
        _runtime_error(f"Type mismatch for operator.__div__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.IDIV:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value // r_value
                return node
        _runtime_error(f"Type mismatch for operator.__idiv__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.MOD:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value % r_value
                return node
        _runtime_error(f"Type mismatch for operator.__mod__({l_ty}, {r_ty}", loc=token.location)
    elif tid == TK.POW:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value ** r_value
                return node
        _runtime_error(f"Type mismatch for operator.__pow__({l_ty}, {r_ty}", loc=token.location)
    return node


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