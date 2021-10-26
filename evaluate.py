from datetime import timedelta

from conversion import c_node2bool, c_node2int, c_node2float
from exceptions import _runtime_error
from literals import DUR
from tokens import TK, TCL

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool']
_INTRINSIC_STR_TYPE = 'str'


def evaluate_literal(node):
    return node.value


def evaluate_binary_operation(node):
    token = node.token
    tid = token.id
    left = node.left
    l_value = left.value
    l_ty = type(left.value).__name__
    right = node.right
    r_value = right.value
    r_ty = type(right.value).__name__

    # UNDONE: need dynamic dispatch here

    if left.token.t_class != TCL.LITERAL or right.token.t_class != TCL.LITERAL:
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
    elif tid == TK.POW:
        if l_ty in _INTRINSIC_VALUE_TYPES:
            if r_ty in _INTRINSIC_VALUE_TYPES:
                node.value = l_value ** r_value
                return node
        _runtime_error(f"Type mismatch for operator.__pow__({l_ty}, {r_ty}", loc=token.location)
    return node


def compare_literal(node):
    tid = node.token.id
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        n = c_node2float(node)
        n.value -= 1
    else:
        n = c_node2int(node)
        n.value -= 1
    return n


def decrement_literal(node):
    tid = node.token.id
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        n = c_node2float(node)
        n.value -= 1
    else:
        n = c_node2int(node)
        n.value -= 1
    return n


def increment_literal(node):
    tid = node.token.id
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        n = c_node2float(node)
        n.value += 1
    else:
        n = c_node2int(node)
        n.value += 1
    return n


def negate_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.INT, TK.FLOT, TK.PCT, TK.DUR]:
        node.value = - node.value
        return node
    elif tid in [TK.BOOL]:
        node.value = not node.value
        return node
    elif tid == TK.STR:
        try:
            v = - int(node.value)
            node.value = v
            node.token.id = TK.INT
            return node
        except ValueError as e:
            pass
    elif tid == TK.EMPTY:
        return node
    _runtime_error("Unsupported type for Unary minus", loc=token.location)


def not_literal(node):
    n = c_node2bool(node)
    n.value = not n.value
    return n
