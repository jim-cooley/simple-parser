
#
# conversion helpers
#
from copy import copy
from datetime import timedelta

from exceptions import _runtime_error
from literals import Bool, Int, Float, _parse_duration
from tokens import TK


# --------------------------------
# General Node conversion helpers
# --------------------------------
def c_node2bool(node):
    tid = node.token.id
    tk = copy(node.token)
    tk.id = TK.BOOL
    tk.value = c_to_bool(tk.value, tid)
    if tk.value is not None:
        tk.lexeme = None
        return Bool(tk)
    _runtime_error("Unsupported type for conversion", loc=tk.location)


def c_node2int(node):
    tid = node.token.id
    tk = copy(node.token)
    tk.id = TK.INT
    tk.value = c_to_int(tk.value, tid)
    if tk.value is not None:
        tk.lexeme = None
        return Int(tk)
    _runtime_error("Unsupported type for conversion", loc=tk.location)


def c_node2float(node):
    tid = node.token.id
    tk = copy(node.token)
    tk.id = TK.FLOT
    tk.value = c_to_float(tk.value, tid)
    if tk.value is not None:
        tk.lexeme = None
        return Float(tk)
    _runtime_error("Unsupported type for conversion", loc=tk.location)


# --------------------------------
# General Value conversion helpers
# --------------------------------
def c_to_bool(val, tid):
    if tid in [TK.BOOL, TK.TRUE, TK.FALSE]:
        return val
    elif tid in [TK.INT, TK.FLOT, TK.PCT]:
        return val != 0
    elif tid in [TK.EMPTY, TK.NONE]:
        return False
    elif tid == TK.STR:
        return _c_str2bool(val)
    else:
        return val != 0


def c_to_dur(val, tid):
    if tid == TK.DUR:
        return val
    elif tid in [TK.FLOT, TK.INT, TK.PCT]:
        return timedelta(seconds=val)
    elif tid in [TK.EMPTY, TK.NONE, TK.FALSE]:
        return timedelta(seconds=0)
    elif tid == TK.STR:
        try:
            v, units = _parse_duration(val)
            return v
        except ValueError as e:
            pass
    return None


def c_to_float(val, tid):
    if tid in [TK.FLOT, TK.PCT]:
        return val
    elif tid in [TK.EMPTY, TK.NONE, TK.FALSE]:
        return float(0)
    elif tid in [TK.BOOL, TK.INT, TK.TRUE]:
        return float(val)
    elif tid == TK.DUR:
        return float(val.total_seconds())
    elif tid == TK.STR:
        try:
            v = float(val)
            return v
        except ValueError as e:
            pass
    return None


def c_to_int(val, tid):
    if tid == TK.INT:
        return val
    elif tid in [TK.EMPTY, TK.NONE, TK.FALSE]:
        return 0
    elif tid in [TK.BOOL, TK.FLOT, TK.PCT, TK.TRUE]:
        return int(val)
    elif tid == TK.DUR:
        return val / timedelta(days=1)   # return integer days.
    elif tid == TK.STR:
        try:
            v = int(val)
            return v
        except ValueError as e:
            pass
    return None


# --------------------------------
# Specific value conversion helpers
# --------------------------------
def _c_str2bool(val):
    try:
        i = int(val)
        return bool(i)
    except ValueError as e:
        pass
    try:
        b = bool(val)
        return b
    except ValueError as e:
        pass
    if val.lower() == 'none' or val.lower() == 'empty':
        return False
    return len(val) > 0

