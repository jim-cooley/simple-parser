import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum
from functools import total_ordering

from environment.scope import Object
from environment.token_class import TCL
from environment.token import Token
from environment.token_ids import TK


class DUR(Enum):
    DAY = 'dy'
    WEEK = 'wk'
    MONTH = 'mo'
    YEAR = 'yr'
    HOUR = 'hr'
    MINUTE = 'min'
    SECOND = 's'


@dataclass
class Literal(Object):
    def __init__(self, value=None, token=None, tid=None, loc=None, parent=None):
        if token is None:
            if tid is not None:
                token = Token(tid=tid, tcl=TCL.LITERAL, val=value, loc=loc)
            else:
                token = Token(tid=TK.OBJECT, tcl=TCL.LITERAL, val=value, loc=loc)
        else:
            tid = token.map2litval() if tid is None else tid
            token.t_class = TCL.LITERAL
            token.id = tid
        super().__init__(value=value, token=token, parent=parent)

    @staticmethod
    def lit(val, tid=None, other=None, loc=None):
        if val is None:
            return LIT_NONE
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


@dataclass
@total_ordering
class Bool(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.BOOL if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = _parse_bool_value(self._value)

    def __lt__(self, other):
        if isinstance(other, bool):
            return True if self._value < other else False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, bool):
            return True if self._value is other else False
        return NotImplemented

    def format(self):
        tk = self.token
        return f'True' if tk._value is not None and tk._value else f'False'


@dataclass
class Category(Literal):
    """
    A Category restricts values to a specified set.  The range of values may be expanded, but the current
    value may not be Set outside the current range.  Strict=False allows new values to be set without
    check.  This is useful for reading from datasets and later inferring the set of categorical values.
    Values are not case sensitive
    """
    def __init__(self, value=None, token=None, loc=None, strict=True):
        tid = TK.CATEGORY if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        self.strict = strict
        self.items = []

    def __len__(self):
        return len(self.items)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = value.lower()
        if value not in self.items:
            if self.strict:
                raise ValueError('Value assigned to Category is out of range')
            self.items.append(value.lower())
        self._value = value

    def append(self, value):
        self.items.append(value)

    def values(self):
        return self.items


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

    def format(self):
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

    def format(self, fmt=None):
        return f'{self._value}'


@dataclass
class Enumeration(Category):
    """
    An Enumeration is a set of categorical values with numeric equivalents.
    """
    def __init__(self, value=None, token=None, loc=None, strict=True, auto_increment=False):
        tid = TK.ENUM if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, loc=loc, strict=strict)
        if self._value is None and token is not None:
            self._value = token.lexeme
        self.auto_increment = auto_increment
        self.seed = -1
        self.items = {}

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = int(value)

    def __len__(self):
        return len(self.items.keys())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = value.lower()
        if value not in self.items:
            if self.strict:
                raise ValueError('Value assigned to Category is out of range')
            if self.auto_increment:
                self.seed += 1
                self.items[value.lower()] = self.seed
        self._value = value

    def to_int(self):
        return self.items[self._value]

    def to_range(self):
        raise NotImplemented()

    def from_category(self, other):
        self.items = {}
        self.seed = -1
        if not isinstance(other, Category):
            raise NotImplemented()
        for item in other.items:
            self.seed += 1
            self.items[item] = self.seed
        return self

    def values(self):
        return self.items.keys()  # the keys are the actual 'values' of the Enumeration. As in range of possible values


@dataclass
class Float(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.FLOT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = float(self._value)

    def format(self, fmt=None):
        return f'{self._value}'


@dataclass
@total_ordering
class Int(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.INT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        self._value = value
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = int(self._value)

    def __lt__(self, other):
        if isinstance(other, int):
            return True if self._value < other else False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, int):
            return True if self._value == other else False
        return NotImplemented

    def format(self, fmt=None):
        return f'{self.qualname} = {self._value}'


@dataclass
class List(Literal):
    def __init__(self, items=None, token=None, loc=None):
        tid = TK.LIST if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=items, token=token, tid=tid, loc=loc)
        self._value = items
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        if self._value is None:
            return True
        return len(self.items) == 0

    def append(self, o):
        self._value.append(o)

    def values(self):
        return self._value

    def format(self):
        if self._value is None:
            return '[]'
        else:
            fstr = ''
            max = (len(self._value)-1)
            for idx in range(0, len(self._value)):
                fstr += f'{self._value[idx]}'
                fstr += ',' if idx < max else ''
            return '[' + f'{fstr}' + ']'


@dataclass
class Percent(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.INT if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme
        if isinstance(self._value, str):
            self._value = float(self._value.replace("%",""))/100

    def format(self, fmt=None):
        return '' if self._value is None else f'{self._value*100} %'


@dataclass
class Set(Literal):
    def __init__(self, items=None, token=None, loc=None):
        tid = TK.SET if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=items, token=token, tid=tid, loc=loc)
        self.items = items if items is not None else {}
        self._value = self.items

    def __getitem__(self, item):
        if type(item).name == 'int':
            return self._values()[item]
        return self._value[item]

    def __setitem__(self, key, value):
        self._value[key] = value

    def __len__(self):
        return len(self.items.keys())

    def is_empty(self):
        return self._value is not None and len(self._values()) > 0

    def keys(self):
        return list(self._value.keys())

    def tuples(self):
        return list(self._value.items())

    def values(self):
        if self._value is None:
            return None
        if type(self._value).__name__ == "list":
            return self._value
        return list(self._members.values())

    def format(self):
        if self._value is None:
            return '{}'
        else:
            fstr = ''
            values = list(self._members.values())
            max = len(values) - 1
            for idx in range(0, max + 1):
                fstr += f'{values[idx]}'
                fstr += ',' if idx < max else ''
            return '{' + f'{fstr}' + '}'


@dataclass
class Str(Literal):
    def __init__(self, value=None, token=None, loc=None):
        tid = TK.STR if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=value, token=token, tid=tid, loc=loc)
        if self._value is None and token is not None:
            self._value = token.lexeme

    def format(self, fmt=None):
        if self._value is None:
            if self.token._value is not None:
                return self.token._value
            elif self.token.lexeme is not None:
                return self.token.lexeme
        return self._value


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

    def format(self, fmt=None):
        fmt = "%H:%M:%S" if fmt is None else fmt
        return self._value.strftime(fmt) if self._value is not None else 'None'


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


# TODO: make these classes if we need to keep them singletons & compare on them, etc
LIT_EMPTY = Set(token=Token(tid=TK.EMPTY, tcl=TCL.LITERAL, lex="{}", val=None))
LIT_NONE = Literal(token=Token(tid=TK.NONE, tcl=TCL.LITERAL, lex="none", val=None))
