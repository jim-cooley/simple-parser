from conversion import c_node2float, c_node2int, c_node2bool, c_to_int, c_to_float, c_to_bool
from environment import Environment
from tokens import TK


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
    Environment.get_logger().runtime_error("Unsupported type for Unary minus", loc=token.location)


def not_literal(val, tid):
    v = c_to_bool(val, tid)
    return not v
