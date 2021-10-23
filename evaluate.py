from datetime import timedelta

from exceptions import _runtime_error
from literals import DUR
from tokens import TK

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool']
_INTRINSIC_STR_TYPE = 'str'


def evaluate_literal(node):
    return node.value


# dispatch tables


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


def negate_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.INT, TK.FLOT, TK.PCT, TK.DUR]:
        node.value = - node.value
        return node
    elif tid in [TK.BOOL]:
        node.value = not node.value
        return node
    elif tid in [TK.STR, TK.EMPTY, TK.TIME]:
        return node
    _runtime_error("Unsupported type for Unary minus", loc=token.location)


def increment_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.BOOL, TK.STR, TK.EMPTY, TK.TIME]:
        return node
    elif tid in [TK.INT, TK.FLOT, TK.PCT]:
        node.value += 1
        return node
    elif tid == TK.DUR:
        u = node.units
        td = timedelta(days=1)
        if u == DUR.DAY:
            td = timedelta(days=1)
        elif u == DUR.WEEK:
            td = timedelta(weeks=1)
        elif u == DUR.MONTH:
            td = timedelta(days=365/12)
        elif u == DUR.YEAR:
            td = timedelta(days=365)
        elif u == DUR.HOUR:
            td = timedelta(hours=1)
        elif u == DUR.MINUTE:
            td = timedelta(minutes=1)
        elif u == DUR.SECOND:
            td = timedelta(seconds=1)
        node.value += td
        return node
    _runtime_error("Unsupported type for Increment operator", loc=token.location)


def decrement_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.BOOL, TK.STR, TK.EMPTY, TK.TIME]:
        return node
    elif tid in [TK.INT, TK.FLOT, TK.PCT]:
        v = (node.value) - 1
        node.value = v
        return node
    elif tid == TK.DUR:
        u = node.units
        td = timedelta(days=1)
        if u == DUR.DAY:
            td = timedelta(days=1)
        elif u == DUR.WEEK:
            td = timedelta(weeks=1)
        elif u == DUR.MONTH:
            td = timedelta(days=365/12)
        elif u == DUR.YEAR:
            td = timedelta(days=365)
        elif u == DUR.HOUR:
            td = timedelta(hours=1)
        elif u == DUR.MINUTE:
            td = timedelta(minutes=1)
        elif u == DUR.SECOND:
            td = timedelta(seconds=1)
        node.value -= td
        return node
    _runtime_error("Unsupported type for Decrement operator", loc=token.location)


def not_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.BOOL, TK.TRUE, TK.FALSE]:
        v = not node.value
        node.value = v
        token.id = TK.BOOL
        return node
    elif tid in [TK.INT, TK.FLOT, TK.PCT]:
        v = node.value
        node.value = not (v != 0)
        return node
    elif tid == TK.EMPTY:
        node.value = True
        return node
    elif tid == TK.STR:
        v = node.value
        return not (v is None or len(v) == 0)
    # UNDONE: check for zero values in Time and TimeDelta
    else:
        node.value = False
        return node
