from datetime import timedelta

from exceptions import _runtime_error
from literals import DUR
from tokens import TK


def evaluate_literal(node):
    return node.value


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
