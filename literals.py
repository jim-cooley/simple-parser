import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta

from tokens import TCL, TK
from tree import Literal

'''
Type Helpers
'''


@dataclass
class Bool(Literal):
    def __init__(self, token, value=None):
        super().__init__(token)
        token.value = value if value is not None else _parse_bool_value(token.lexeme)

    def format(self):
        tk = self.token
        return f'True' if tk.value is not None and tk.value else f'False'


@dataclass
class DateTime(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = _parse_date_value(token.lexeme)

    def format(self):
        return f'{self.value}'


@dataclass
class Duration(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = _parse_duration(token.lexeme)

    def total_seconds(self):
        return self.value.total_seconds()

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Float(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = float(token.lexeme)

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Int(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = int(token.lexeme)

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class List(Literal):
    def __init__(self, token, mlist=None):
        super().__init__(token)
        token.id = TK.LIST
        token.t_class = TCL.LIST
        token.value = None if mlist is None else mlist
        self.members = mlist

    def format(self):
        if self.members is None:
            return '[]]'
        else:
            return '[' + self.members + ']'


@dataclass
class Percent(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = float(token.lexeme.replace("%",""))/100

    def format(self, fmt=None):
        return f'{self.value*100} %'


@dataclass
class Set(Literal):
    def __init__(self, token, mlist=None):
        super().__init__(token)
        token.id = TK.SET
        token.t_class = TCL.SET
        token.value = None if mlist is None else mlist
        self.members = mlist

    def format(self):
        if self.members is None:
            return '{}'
        else:
            return '{' + self.members + '}'


@dataclass
class Str(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = token.lexeme

    def format(self, fmt=None):
        return self.value


@dataclass
class Time(Literal):
    def __init__(self, token):
        super().__init__(token)
        token.value = _parse_time_value(token.lexeme)

    def format(self, fmt=None):
        fmt = "%H:%M:%S" if fmt is None else fmt
        return self.value.strftime(fmt)


def _parse_bool_value(lex):
    lex = lex.lower().strip()
    return True if lex == 'true' else False


def _parse_time_value(lex):
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


def _parse_date_value(lex):
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