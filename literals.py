import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum

from tokens import TCL, TK, Token
from scope import Literal

'''
Type Helpers
'''


class DUR(Enum):
    DAY = 'dy'
    WEEK = 'wk'
    MONTH = 'mo'
    YEAR = 'yr'
    HOUR = 'hr'
    MINUTE = 'min'
    SECOND = 's'


@dataclass
class Bool(Literal):
    def __init__(self, token, value=None):
        super().__init__(token=token)
        if value is not None:
            token.value = value
        if token.value is None:
            token.value = _parse_bool_value(token.lexeme)

    def format(self):
        tk = self.token
        return f'True' if tk.value is not None and tk.value else f'False'


@dataclass
class DateTime(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        if token.value is None:
            token.value = _parse_date_value(token.lexeme)

    def format(self):
        return f'{self.value}'


@dataclass
class Duration(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        if token.value is None:
            token.value, self.units = _parse_duration(token.lexeme)

    def total_seconds(self):
        return self.value.total_seconds()

    def units(self):
        return self.units

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Float(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        if token.value is None:
            token.value = float(token.lexeme)

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class Int(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        if token.value is None:
            token.value = int(token.lexeme)

    def format(self, fmt=None):
        return f'{self.value}'


@dataclass
class List(Literal):
    def __init__(self, token, items=None):
        super().__init__(token=token)
        token.t_class = TCL.LITERAL
        token.value = None if items is None else items
        self.value = items

    def __getitem__(self, index):
        return self.values()[index]

    def __setitem__(self, index, value):
        self.value[index] = value

    def is_empty(self):
        return self.value is not None and len(self.values()) > 0

    def append(self, o):
        self.value.append(o)

    def len(self):
        return len(self.values)

    def values(self):
        return self.value

    def format(self):
        if self.value is None:
            return '[]'
        else:
            fstr = ''
            max = (len(self.value)-1)
            for idx in range(0, len(self.value)):
                fstr += f'{self.value[idx]}'
                fstr += ',' if idx < max else ''
            return '[' + f'{fstr}' + ']'


@dataclass
class Percent(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        token.value = float(token.lexeme.replace("%",""))/100

    def format(self, fmt=None):
        return '' if self.value is None else f'{self.value*100} %'


@dataclass
class Set(Literal):
    def __init__(self, token, items=None):
        super().__init__(token=token)
        self.items = items if items is not None else {}
        self.value = self.items
        token.id = TK.SET if len(self.items) > 0 else TK.EMPTY
        token.t_class = TCL.LITERAL

    def __getitem__(self, item):
        if type(item).name == 'int':
            return self.values()[item]
        return self.value[item]

    def __setitem__(self, key, value):
        self.value[key] = value

    def is_empty(self):
        return self.value is not None and len(self.values()) > 0

    def keys(self):
        return list(self.value.keys())

    def tuples(self):
        return list(self.value.items())

    def values(self):
        if self.value is None:
            return None
        if type(self.value).__name__ == "list":
            return self.value
        return list(self._symbols.values())

    def format(self):
        if self.value is None:
            return '{}'
        else:
            fstr = ''
            values = list(self._symbols.values())
            max = len(values) - 1
            for idx in range(0, max + 1):
                fstr += f'{values[idx]}'
                fstr += ',' if idx < max else ''
            return '{' + f'{fstr}' + '}'


@dataclass
class Str(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        token.value = token.lexeme

    def format(self, fmt=None):
        if self.value is None:
            if self.token.value is not None:
                return self.token.value
            elif self.token.lexeme is not None:
                return self.token.lexeme
        return self.value


@dataclass
class Time(Literal):
    def __init__(self, token):
        super().__init__(token=token)
        token.value = _parse_time_value(token.lexeme)

    def format(self, fmt=None):
        fmt = "%H:%M:%S" if fmt is None else fmt
        return self.value.strftime(fmt) if self.value is not None else 'None'


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
    units = _parse_duration_units(lex.replace(digits, "").strip())
    n = float(digits)
    dur = None
    if units == DUR.DAY:
        dur = timedelta(days=n)
    elif units == DUR.WEEK:
        dur = timedelta(days=7*n)
    elif units == DUR.MONTH:
        dur = timedelta(days=28*n)
    elif units == DUR.YEAR:
        dur = timedelta(days=365*n)
    elif units == DUR.HOUR:
        dur = timedelta(hours=n)
    elif units == DUR.MINUTE:
        dur = timedelta(minutes=n)
    elif units == DUR.SECOND:
        dur = timedelta(seconds=n)
    return dur, units


def _parse_duration_units(units):
    dur = DUR.DAY
    if units in ("d", "dy", "day", "days"):
        dur = DUR.DAY
    elif units in ("w", "wk", "week"):
        dur = DUR.WEEK
    elif units in ("M", "mo", "mos", "month", "months"):
        dur = DUR.MONTH
    elif units in ("y", "yr", "yrs", "year", "years"):
        dur = DUR.YEAR
    elif units in ("h", "hr", "hours"):
        dur = DUR.HOUR
    elif units in ("m", "min", "mins", "minutes"):
        dur = DUR.MINUTE
    elif units in ("s", "sec", "seconds"):
        dur = DUR.SECOND
    return dur


LIT_EMPTY_SET = Set(Token(tid=TK.EMPTY, tcl=TCL.LITERAL, lex="{}", val=None))
LIT_NONE = Literal(Token(tid=TK.NONE, tcl=TCL.LITERAL, lex="none", val=None))
