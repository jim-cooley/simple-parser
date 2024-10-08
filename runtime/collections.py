from dataclasses import dataclass
from enum import Enum

from runtime.exceptions import runtime_error
from runtime.literals import Literal
from runtime.scope import Block
from runtime.token import Token
from runtime.token_ids import TK
from runtime.tree import Generate


class DUR(Enum):
    DAY = 'dy'
    WEEK = 'wk'
    MONTH = 'mo'
    YEAR = 'yr'
    HOUR = 'hr'
    MINUTE = 'min'
    SECOND = 's'


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
        self._items = []

    def __len__(self):
        return len(self._items)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = value.lower()
        if value not in self._items:
            if self.strict:
                raise ValueError('Value assigned to Category is out of range')
            self._items.append(value.lower())
        self._value = value

    def append(self, value):
        self._items.append(value)

    def items(self):
        return self._items  # UNDONE: turn this into iterator

    def values(self):
        return self._items


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
        self._items = {}

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = int(value)

    def __len__(self):
        return len(self._items.keys())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = value.lower()
        if value not in self._items:
            if self.strict:
                raise ValueError('Value assigned to Category is out of range')
            if self.auto_increment:
                self.seed += 1
                self._items[value.lower()] = self.seed
        self._value = value

    def to_int(self):
        return self._items[self._value]

    def to_range(self):
        raise NotImplemented()

    def from_category(self, other):
        self._items = {}
        self.seed = -1
        if not isinstance(other, Category):
            raise NotImplemented()
        for item in other._items:
            self.seed += 1
            self._items[item] = self.seed
        return self

    def values(self):
        return self._items.keys()  # the keys are the actual 'values' of the Enumeration. As in range of possible values


@dataclass
class List(Literal):
    def __init__(self, items=None, token=None, loc=None):
        tid = TK.LIST if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=items, token=token, tid=tid, loc=loc)
        self._value = items
        self._items = items

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        if self._items is not None:
            return len(self._items)
        return 0

    @staticmethod
    def EMPTY(loc=None):
        return List(items=None, token=Token.LIST(loc=loc))

    def is_empty(self):
        if self._value is None:
            return True
        return len(self._items) == 0

    def append(self, o):
        self._value.append(o)

    def items(self):    # UNDONE: should be iterator
        """
        items is a list of AST 'items' used to construct this list instance.
        """
        return self._items

    def values(self):
        """
        Values is the list values themselves.
        """
        return self._value

    def set_values(self, values):
        self._value = values

    def format(self, brief=True):
        if self._value is None:
            return '[]'
        else:
            if not brief:
                fstr = ''
                max = (len(self._value)-1)
                for idx in range(0, len(self._value)):
                    fstr += f'{self._value[idx]}'
                    fstr += ',' if idx < max else ''
            else:
                fstr = f'count={len(self._value)}'
            return 'List[' + f'{fstr}' + ']'


@dataclass
class Set(Literal):
    def __init__(self, items=None, token=None, loc=None):
        tid = TK.SET if token is None else token.map2litval()
        loc = loc if token is None else token.location
        super().__init__(value=items, token=token, tid=tid, loc=loc)
        self._items = items if items is not None else {}
        self._value = self._items

    def __getitem__(self, item):
        if type(item).name == 'int':
            return self.value()[item]
        return self._value[item]

    def __setitem__(self, key, value):
        self._value[key] = value

    def __len__(self):
        return len(self._items)

    @staticmethod
    def EMPTY(loc=None):
        return Set(token=Token.EMPTY(loc=loc))

    def is_empty(self):
        return self._value is not None and len(self.values()) > 0

    def items(self):    # UNDONE: should be iterator
        return self._items

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

    def format(self, brief=True):
        if self._value is None:
            return '{}'
        else:
            values = list(self._members.values())
            if not brief:
                fstr = ''
                max = len(values) - 1
                for idx in range(0, max + 1):
                    fstr += f'{values[idx]}'
                    fstr += ',' if idx < max else ''
            else:
                fstr = f'count={len(values) - 1}'
            return 'Set{' + f'{fstr}' + '}'


# --------------------------------------------------
#              S U B  C L A S S E S
# --------------------------------------------------
# Dict when there are named elements (Series maybe?)
@dataclass
class Dict(Set):
    def __init__(self, items=None, token=None, loc=None):
        token = Token.DICT(loc=loc)
        super().__init__(items=items, token=token, loc=loc)


# Specialized derivative of List
@dataclass
class Tuple(List):
    def __init__(self, items=None, token=None, loc=None):
        token = token or Token.TUPLE(loc=loc)
        super().__init__(items, token, loc)


# Named Tuple when there are named items (k:v)
@dataclass
class NamedTuple(Tuple):
    def __init__(self, items=None, token=None, loc=None):
        token = Token.NAMEDTUPLE(loc=loc)
        super().__init__(items=items, token=token, loc=loc)


def build_collection(tid=None, items=None, loc=None):
    is_literal = True
    for item in items:
        if not isinstance(item, Literal):
            is_literal = False
    if is_literal:
        return lit_collection(tid=tid, items=items, loc=loc)
    else:
        if tid in [TK.DATAFRAME, TK.DICT, TK.LIST, TK.NAMEDTUPLE, TK.SERIES, TK.SET, TK.TUPLE]:
            return Generate(tid, items=items, loc=loc)
        else:
            runtime_error("Unsupported target type for collection")


def lit_collection(tid=None, items=None, loc=None):
    if tid == TK.LIST:
        return List(items=items, loc=loc)
    elif tid == TK.TUPLE:
        return Tuple(items=items, loc=loc)
    elif tid == TK.NAMEDTUPLE:
        return NamedTuple(items=items, loc=loc)
    elif tid == TK.BLOCK:
        return Block(items=items, loc=loc)
    elif tid == TK.SET:
        return Set(items=items, loc=loc)
    elif tid == TK.DICT:
        return Dict(items=items, loc=loc)
    elif tid == TK.SERIES:
        return Generate(TK.SERIES, items=items, loc=loc)
    elif tid == TK.DATAFRAME:
        return Generate(TK.DATAFRAME, items=items, loc=loc)
    else:
        runtime_error("Unsupported target type for collection")
