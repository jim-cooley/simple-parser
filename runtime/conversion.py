
#
# conversion helpers
#
from copy import copy
from datetime import timedelta

from runtime.exceptions import runtime_error
from runtime.literals import Bool, Int, Float, _parse_duration
from runtime.token_data import native2tkid
from runtime.token_ids import TK


# --------------------------------
# "Box" / "Unbox" Helpers
# --------------------------------
def c_box(u, val):
    if hasattr(u, 'value'):
        u.value = val
    else:
        u = val
    return u


def c_unbox(u):
    if hasattr(u, 'value'):
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
# General type conversion helpers
# --------------------------------
def c_to_bool(val, tid):
    """
    Convert a value to a bool.  Value may be an intrinsic (platform) or runtime Object

    :param val:
    :type val: any
    :param tid:
    :type tid: TK
    :return: bool()
    """
    if val is None:
        return False
    tid = tid if tid is not None else c_type(val)
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
    """
    Convert a value to a Duration.  Value may be an intrinsic (platform) or another runtime Object.  String parsing
    is supported via _parse_duration()

    :param val:
    :type val: any
    :param tid:
    :type tid: TK
    :return: Duration()
    """
    if val is None:
        return timedelta(seconds=0)
    tid = tid if tid is not None else c_type(val)
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
    """
    Convert a value to a float.  Value may be an intrinsic (platform) or runtime Object

    :param val:
    :type val: any
    :param tid:
    :type tid: TK
    :return: float()
    """
    if val is None:
        return float(0)
    tid = tid if tid is not None else c_type(val)
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
    """
    Converts a value to an int(). The value may be another intrinsic or it may be a structured type descending from
    Object.

    :param val: value to convert
    :param tid: optional: type id of value to convert
    :type tid: TK
    :return: int()
    """
    if val is None:
        return 0
    tid = tid if tid is not None else c_type(val)
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
    """
    Converts a value to a bool(). The value may be another intrinsic or it may be a structured type descending from
    Object.

    :param val: value to convert
    :type val: str
    :return: bool
    """
    if val is None:
        return False
    v = val.lower()
    try:
        i = int(v)
        return bool(i)
    except Exception as e:
        pass
    if v == 'true':
        return True
    if v == 'false'\
            or v == 'none' \
            or v == 'empty'\
            or v == 'nil':
        return False
    try:
        b = bool(v)
        return b
    except Exception as e:
        pass
    return len(val) > 0

