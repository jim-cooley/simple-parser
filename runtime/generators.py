from copy import copy, deepcopy
from datetime import timedelta
from enum import IntEnum, unique, auto

import numpy

from runtime.conversion import c_unbox, c_sign, c_type
from runtime.time import get_dt_now
from runtime.series import Series
from runtime.token_ids import TK

NAME_PROPERTY = 'name'
INDEX_PROPERTY = 'index'
COLUMNS_PROPERTY = 'columns'

_DEFAULT_SERIES_ITEMS = {
    'name': None,
    'index': None,
}

_DEFAULT_DATAFRAME_ITEMS = {
    'name': None,
    'index': None,
    'columns': None,
}


# gives a common super-type to all instances: isinstance(generator, FocalGenerator) == True
class FocalGenerator:
    pass


class RangeGenerator(FocalGenerator):
    @unique
    class SELECTOR(IntEnum):
        ZEROS = 0
        ONES = 1
        NAN = auto()
        NONE = auto()

    def __init__(self, start=None, end=None, width=None, step=None, selector=None):
        """
        RangeGenerator - creates a deferred range iterator
        :param start: start of range, or 0 if not specified
        :param end: end of range.  if only one parameter specified, it is end.  If selector is specified
        :param width: width of range.  width is used for clarity in combination with selector.
        :param step: step value for iterator or 1 if not specified.
        :param selector: indicates special range: zeros, ones, etc.  See SELECTOR
        :type selector: SELECTOR
        """
        self.start = start if start is not None else 0
        self.end = end if end is not None else width
        self.step = step or 1
        self.current = None
        self.selector = selector
        self.tid = c_type(self.start)

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        if self.tid != TK.DUR:
            if self.selector is None:
                current = self.current
                self.current += self.step
                return current
            else:
                if self.selector == self.SELECTOR.ZEROS:
                    return 0
                elif self.selector == self.SELECTOR.ONES:
                    return 1
                elif self.selector == self.SELECTOR.NAN:
                    return numpy.NaN
                elif self.selector == self.SELECTOR.NONE:
                    return None
                else:
                    raise StopIteration
        else:
            _now = get_dt_now()
            if self.selector is None:
                current = self.current
                self.current += self.step
                return current + _now
            else:
                if self.selector == self.SELECTOR.ZEROS:
                    return _now
                elif self.selector == self.SELECTOR.ONES:
                    return timedelta(days=1)
                elif self.selector == self.SELECTOR.NAN:
                    return numpy.NaN
                elif self.selector == self.SELECTOR.NONE:
                    return None
                else:
                    raise StopIteration

    def getall(self):
        return list(self)


# later this will hold more complex construction logic and support iteration
class SeriesGenerator(FocalGenerator):
    def __init__(self, name=None, selector=None, values=None, index=None):
        self.name = name
        self.values = values
        self.index = index
        self.series = selector  # special series designator

    def getall(self):
        return Series(name=self.name, index=self.index, values=self.values)


def generate_dataframe(env, args):
    return None


def generate_dict(env, args):
    return None


def generate_list(env, args):
    return args.values()


def generate_named_tuple(env, args):
    return None


# UNDONE: right now we are materializing the generator product, but we could pass the generator back.
# UNDONE: just need to make sure that works in all cases.
def generate_range(env, args):
    start = end = _zero = 0
    args = list(filter(None.__ne__, args))
    ty = c_type(args[0])
    if ty == TK.DUR:
        step = timedelta(days=1)
        _zero = timedelta(days=0)
        start = end = _zero
    elif ty not in [TK.INT, TK.FLOT]:
        raise TypeError(f"Unsupported range type TK.{TK(ty).name}")
    else:
        step = 1
    if hasattr(args, 'end'):
        end = args.end
    elif len(args) == 1:
        end = args[0]
        if c_sign(end) < 0:
            start = args[0]
            end = _zero
    if hasattr(args, 'width'):
        width = args.width
    if hasattr(args, 'start'):
        start = args.start
    elif len(args) > 1:
        start = args[0]
        end = args[1]
    if hasattr(args, 'step'):
        step = args.step
    elif len(args) > 2:
        step = args[2]
    r = RangeGenerator(start=start, end=end, step=step)
    return r.getall()


def generate_series(env, args):
    name = None
    index = None
    if hasattr(args, NAME_PROPERTY):
        name = copy(c_unbox(args.name))
    if hasattr(args, INDEX_PROPERTY):
        index = deepcopy(c_unbox(args.index))
    args.remove([NAME_PROPERTY, INDEX_PROPERTY])
    gen = SeriesGenerator(name=name, values=args.dict(), index=index)
    series = gen.getall()
    return series


def generate_set(env, args):
    return None


def generate_tuple(env, args):
    return None


