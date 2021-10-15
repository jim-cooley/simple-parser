# abstract syntax trees:
import re
from dataclasses import dataclass
from datetime import time, datetime, timedelta

from tokens import TCL, TK


@dataclass
class AST(object):
    def __getattr__(self, item):
        if item == 'properties':
            return self.token.properties
        elif item == 'value':
            return self.token.value
        pass


@dataclass
class BinOp(AST):
    def __init__(self, token, left, right):
        token.t_class = TCL.BINOP
        self.left = left
        self.right = right
        self.token = token
        self.op = token.id


@dataclass
class DateTime(AST):
    def __init__(self, token):
        token.value = _parse_date_value(token.lexeme)
        token.t_class = TCL.LITERAL
        self.token = token


@dataclass
class Duration(AST):
    def __init__(self, token):
        token.value = _parse_duration(token.lexeme)
        token.t_class = TCL.LITERAL
        self.token = token

    def total_seconds(self):
        return self.value.total_seconds()

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Float(AST):
    def __init__(self, token):
        token.value = float(token.lexeme)
        token.t_class = TCL.LITERAL
        self.token = token

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class FnCall(AST):
    def __init__(self, token, plist):
        self.token = token
        self.parameter_list = plist


@dataclass
class Ident(AST):
    def __init__(self, token):
        self.token = token


@dataclass
class Int(AST):
    def __init__(self, token):
        token.value = int(token.lexeme)
        token.t_class = TCL.LITERAL
        self.token = token

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Percent(AST):
    def __init__(self, token):
        token.value = float(token.lexeme.replace("%",""))/100
        token.t_class = TCL.LITERAL
        self.token = token

    def format(self, fmt=None):
        return f'{self.value*100} %'


@dataclass
class PropCall(AST):
    def __init__(self, token, member, plist):
        self.token = token
        self.member = member
        self.parameter_list = Seq(None, plist)


@dataclass
class PropRef(AST):
    def __init__(self, token, prop):
        self.identifier = token
        self.member = prop


@dataclass
class Seq(AST):
    def __init__(self, token, slist):
        self.token = token
        self.sequence = slist


@dataclass
class Set(AST):
    def __init__(self, token, mlist):
        token.id = TK.SET
        token.t_class = TCL.SET
        self.token = token
        self.members = mlist


@dataclass
class Str(AST):
    def __init__(self, token):
        token.value = token.lexeme
        token.t_class = TCL.LITERAL
        self.token = token

    def format(self, fmt=None):
        return self.value


@dataclass
class Time(AST):
    def __init__(self, token):
        token.value = _parse_time_value(token.lexeme)
        token.t_class = TCL.LITERAL
        self.token = token

    def format(self, fmt=None):
        fmt = "%H:%M:%S" if fmt is None else fmt
        return self.value.strftime(fmt)


@dataclass
class UnaryOp(AST):
    def __init__(self, token, expr):
        token.t_class = TCL.UNARY
        self.token = token
        self.op = token.id
        self.expr = expr


class NodeVisitor(object):
    def visit(self, node):
        if node is not None:
            method_name = 'visit_' + type(node).__name__
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


# Helpers
def _parse_time_value(lex, format=None):
    if format is not None:
        return datetime.strptime(lex, format).time()
    lex = lex.lower().replace('am', ' AM').replace('a', ' AM').replace('pm', ' PM').replace('p', ' PM')
    try:
        return time.fromisoformat(lex)
    except ValueError as e:
        pass
    for format in ("%-H:%M:%S", "%H:%M:%S", "%-I:%M:%S %p", "%I:%M:%S %p", "%-H:%M", "%H:%M",
                   "%-I:%M %p", "%I:%M %p", "%H:%M:%S.%f", "%I:%M:%S.%f %p"):
        try:
            return datetime.strptime(lex, format).time()
        except ValueError as e:
            continue
    raise Exception(f'Format Error: {lex} not a date/time value.')


def _parse_date_value(lex, format=None):
    if format is not None:
        return datetime.strptime(lex, format).time()
    lex = lex.lower().replace('am', ' AM').replace('a', ' AM').replace('pm', ' PM').replace('p', ' PM')

    try:
        return datetime.fromisoformat(lex)
    except ValueError as e:
        pass
    try:
        return datetime.fromtimestamp(lex)
    except ValueError as e:
        pass

    for format in ("%-H:%M:%S", "%H:%M:%S", "%-I:%M:%S %p", "%I:%M:%S %p",
                   "%-H:%M", "%H:%M", "%-I:%M %p", "%I:%M %p", "%H:%M:%S.%f",
                   "%I:%M:%S.%f %p",
                   "%d/%m/%y %H:%M", "%a %d/%m/%y %H:%M", "%x", "%X", "%x %X"):
        try:
            return datetime.strptime(lex, format).time()
        except ValueError as e:
            continue
    raise Exception(f'Format Error: {lex} not a date/time value.')


def _parse_duration(lex):
    p = re.compile("[0-9.]+")
    digits = p.match(lex).group()
    units = lex.replace(digits, "").strip().lower()
    n = float(digits)
    dur = None
    if units in ("d", "dy", "day", "days"):
        dur = timedelta(days=n)
    elif units in ("w", "wk", "week"):
        dur = timedelta(days=7*n)
    elif units in ("m", "mo", "mos", "month", "months"):
        dur = timedelta(days=30*n)
    elif units in ("y", "yr", "yrs", "year", "years"):
        dur = timedelta(days=365*n)
    elif units in ("h", "hr", "hours"):
        dur = timedelta(hours=n)
    elif units in ("min", "mins", "minutes"):
        dur = timedelta(minutes=n)
    elif units in ("s", "sec", "seconds"):
        dur = timedelta(seconds=n)
    return dur
