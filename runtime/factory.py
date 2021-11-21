from datetime import datetime, timedelta

from runtime.collections import Set, List
from runtime.literals import Literal, Bool, Float, Int, Str
from runtime.time import Time, Duration


def lit_empty(loc=None):
    return Set.EMPTY(loc=loc)


def lit_list_empty(loc=None):
    return List.EMPTY(loc=loc)


def to_lit(val, tid=None, other=None, loc=None):
    if val is None:
        return Literal.NONE(loc=loc)
    if other is not None:
        if other.token is not None:
            loc = other.token.location
    if tid is not None:
        return Literal(value=val, tid=tid)
    elif isinstance(val, bool):
        return Bool(value=val, loc=loc)
    elif isinstance(val, datetime):
        return Time(value=val)
    elif isinstance(val, float):
        return Float(value=val)
    elif isinstance(val, int):
        return Int(value=val)
    elif isinstance(val, str):
        return Str(value=val)
    elif isinstance(val, timedelta):
        return Duration(value=val)
    else:
        return Literal(value=val)
