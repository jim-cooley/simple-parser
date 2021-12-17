from runtime.conversion import c_to_int, c_to_float, c_to_bool, c_type
from runtime.exceptions import runtime_error
from runtime.pandas import df_negate, pdi_union
from runtime.token_ids import TK


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
    elif tid == TK.DATAFRAME:
        return df_negate(val)
    elif tid == TK.STR:
        try:
            v = - int(val)
            return v
        except ValueError as e:
            pass
    elif tid == TK.EMPTY:
        return val
    runtime_error("Unsupported type for Unary minus", loc=None)


def union_literal(val, tid):
    if tid in [TK.INT, TK.FLOT, TK.PCT, TK.DUR, TK.BOOL, TK.STR, TK.EMPTY]:
        return val
    if tid in [TK.DATAFRAME, TK.SERIES]:
        return val.any()
    if tid == TK.LIST:
        tid = c_type(val[0])
    if tid in [TK.DATAFRAME, TK.SERIES]:
        return pdi_union(val[0], val[1])
    return val


def is_true(val, tid):
    v = c_to_bool(val, tid)
    return v is True


def is_false(val, tid):
    return not is_true(val, tid)


def not_literal(val, tid):
    v = c_to_bool(val, tid)
    return not v
