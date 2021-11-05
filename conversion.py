
#
# conversion helpers
#
from copy import copy
from datetime import timedelta

from exceptions import runtime_error
from literals import Bool, Int, Float, _parse_duration
from scope import Object
from tokens import TK, native2tkid


# --------------------------------
# General Value conversion helpers
# --------------------------------
def c_box(u, val):
    if hasattr(u, 'value'):
        u.value = val
    else:
        u = val
    return u


def c_unbox(u):
    if isinstance(u, Object):
        u = u.value
    if getattr(u, 'value', False):
        u = u.value
    return u


def c_type(u):
    tid = TK.NONE
    if getattr(u, 'token', False):
        tid = u.token.id
        return tid
    v = c_unbox(u)
    ty = type(v).__name__
    if ty in native2tkid:
        tid = native2tkid[ty]
    return tid


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
    runtime_error("Unsupported type for conversion", loc=tk.location)


def c_node2int(node):
    tid = node.token.id
    tk = copy(node.token)
    tk.id = TK.INT
    tk.value = c_to_int(tk.value, tid)
    if tk.value is not None:
        tk.lexeme = None
        return Int(tk)
    runtime_error("Unsupported type for conversion", loc=tk.location)


def c_node2float(node):
    tid = node.token.id
    tk = copy(node.token)
    tk.id = TK.FLOT
    tk.value = c_to_float(tk.value, tid)
    if tk.value is not None:
        tk.lexeme = None
        return Float(tk)
    runtime_error("Unsupported type for conversion", loc=tk.location)


def c_to_bool(val, tid):
    if val is None:
        return False
    if tid in [TK.NATIVE, TK.IDNT]:
        return val is True
    elif tid in [TK.BOOL, TK.TRUE, TK.FALSE]:
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
    if val is None:
        return timedelta(seconds=0)
    if tid in [TK.NATIVE, TK.IDNT]:
        ty = type(val).__name__
        if ty == 'timedelta':
            return val
        elif ty == 'int' or ty == 'float':
            return timedelta(days=val)
        elif ty == 'str':
            return _parse_duration(val)
    elif tid == TK.DUR:
        return val
    elif tid in [TK.FLOT, TK.INT, TK.PCT]:
        return timedelta(days=val)
    elif tid in [TK.EMPTY, TK.NONE, TK.FALSE]:
        return timedelta(days=0)
    elif tid == TK.STR:
        try:
            v, units = _parse_duration(val)
            return v
        except ValueError as e:
            pass
    return None


def c_to_float(val, tid):
    if val is None:
        return float(0)
    if tid in [TK.NATIVE, TK.IDNT]:
        ty = type(val).__name__
        if ty == 'float':
            return val
        else:
            try:
                v = float(val)
                return v
            except ValueError as e:
                pass
    elif tid in [TK.FLOT, TK.PCT]:
        return val
    elif tid in [TK.EMPTY, TK.NONE, TK.FALSE]:
        return float(0)
    elif tid in [TK.BOOL, TK.INT, TK.TRUE]:
        return float(val)
    elif tid == TK.DUR:
        return float(val.total_seconds()) / 86400
    elif tid == TK.STR:
        try:
            v = float(val)
            return v
        except ValueError as e:
            pass
    return None


def c_to_int(val, tid):
    if val is None:
        return 0
    if tid == TK.INT:
        return val
    elif tid in [TK.NATIVE, TK.IDNT]:
        ty = type(val).__name__
        if ty == 'int':
            return val
        else:
            try:
                v = int(val)
                return v
            except ValueError as e:
                pass
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
    if val is None:
        return False
    try:
        i = int(val)
        return bool(i)
    except Exception as e:
        pass
    try:
        b = bool(val)
        return b
    except Exception as e:
        pass
    if val.lower() == 'none' or val.lower() == 'empty':
        return False
    return len(val) > 0

