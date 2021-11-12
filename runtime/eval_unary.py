from environment.conversion import c_to_int, c_to_float, c_to_bool
from environment.exceptions import runtime_error
from environment.token_ids import TK


def apply_chain(l_expr, tid):
    pass


def decrement_literal(val, tid):
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        v = c_to_float(val, tid)
        v -= 1
    else:
        v = c_to_int(val, tid)
        v -= 1
    return v


def increment_literal(val, tid):
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        v = c_to_float(val, tid)
        v += 1
    else:
        v = c_to_int(val, tid)
        v += 1
    return v


def negate_literal(val, tid):
    if tid in [TK.INT, TK.FLOT, TK.PCT, TK.DUR]:
        val = - val
        return val
    elif tid in [TK.BOOL]:
        val = not val
        return val
    elif tid == TK.STR:
        try:
            v = - int(val)
            return v
        except ValueError as e:
            pass
    elif tid == TK.EMPTY:
        return val
    runtime_error("Unsupported type for Unary minus", loc=None)


def is_true(val, tid):
    v = c_to_bool(val, tid)
    return v is True


def is_false(val, tid):
    return not is_true(val, tid)


def not_literal(val, tid):
    v = c_to_bool(val, tid)
    return not v
