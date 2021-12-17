
#
# conversion helpers
#
from datetime import timedelta

from runtime.collections import List
from runtime.time import _parse_duration
from runtime.token_data import type2tid
from runtime.token_ids import TK


_type2native = {
    'Block': 'block',
    'Bool': 'bool',
    'bool': 'bool',
    'DataFrame': 'dataframe',
    'DateTime': 'datetime',
    'datetime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'float': 'float',
    'Function': 'function',
    'Ident': 'object',
    'Int': 'int',
    'IntrinsicFunction': 'function',
    'int': 'int',
    'List': 'list',
    'list': 'list',
    'ndarray': 'ndarray',
    'NoneType': 'none',
    'Object': 'object',
    'object': 'object',
    'Percent': 'float',
    'Range': 'range',
    'Series': 'series',
    'Set': 'set',
    'Str': 'str',
    'str': 'str',
    'Time': 'datetime',
    'timedelta': 'timedelta',
}


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


def c_array_unbox(a):
    if not isinstance(a[0], list) and not isinstance(a[0], List):
        return [c_unbox(x) for x in a]
    else:
        for x in a:
            a[x] = c_array_unbox(x)
            return a


def c_type(u):
    tid = TK.NONE
    if hasattr(u, 'tid'):
        tid = u.tid
        if tid is not None:
            return tid
    v = c_unbox(u)
    ty = type(v).__name__
    if ty in _type2native:
        ty = _type2native[ty]
    if ty in type2tid:
        tid = type2tid[ty]
    return tid


def c_sign(u):
    v = c_to_int(c_unbox(u))
    if v < 0:
        return -1
    elif v > 0:
        return 1
    else:
        return 0


# --------------------------------
# General type conversion helpers
# --------------------------------
def c_to_bool(val, tid=None):
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
    if tid in [TK.NATIVE, TK.IDENT]:
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


def c_to_dur(val, tid=None):
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
    if tid in [TK.NATIVE, TK.IDENT]:
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


def c_to_float(val, tid=None):
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
    if tid in [TK.NATIVE, TK.IDENT]:
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


def c_to_int(val, tid=None):
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
    val = c_unbox(val)
    if tid == TK.NATIVE or tid is None:
        tid = c_type(val)
    if tid == TK.INT:
        return val
    elif tid == TK.IDENT:
        ty = type(val).__name__
        if ty == 'int':
            return val
        else:
            try:
                v = int(val)
                return v
            except (ValueError, TypeError) as e:
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
def _c_str2bool(val=None):
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

