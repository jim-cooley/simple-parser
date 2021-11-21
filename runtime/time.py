import re
from dataclasses import dataclass
from datetime import time, datetime, timedelta

from runtime.literals import Literal
from runtime.collections import DUR
from runtime.token_ids import TK


@dataclass
class DateTime(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.TIME if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = _parse_date_value(self._value)

    def format(self, brief=True):
        return f'{self._value}'


@dataclass
class Duration(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.DUR if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value, self.units = _parse_duration(self._value)

    def total_seconds(self):
        return self._value.total_seconds()

    def units(self):
        return self.units

    def format(self, brief=True, fmt=None):
        return f'{self._value}'


@dataclass
class Time(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.TIME if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = _parse_time_value(self._value)

    def format(self, fmt=None, brief=True):
        fmt = "%H:%M:%S" if fmt is None else fmt
        return self._value.strftime(fmt) if self._value is not None else 'None'


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
