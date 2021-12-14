from copy import copy, deepcopy
import datetime as dt
from enum import IntEnum, unique, auto

import numpy
import pandas as pd

from runtime.conversion import c_unbox, c_sign, c_type
from runtime.time import get_dt_now, _parse_date_value, _parse_time_value, Time
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


class DataframeGenerator(FocalGenerator):
    def __init__(self, name=None, selector=None, values=None, columns=None, index=None):
        self.name = name
        self.values = values
        self.columns = columns
        self.index = index
        self.series = selector  # special series designator

    def getall(self):
        return pd.DataFrame(data=self.values, columns=self.columns, index=self.index)


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
        if self.current >= self.end:
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
                    return dt.timedelta(days=1)
                elif self.selector == self.SELECTOR.NAN:
                    return numpy.NaN
                elif self.selector == self.SELECTOR.NONE:
                    return None
                else:
                    raise StopIteration

    def getall(self):
        return list(self)


class SeriesGenerator(FocalGenerator):
    def __init__(self, name=None, selector=None, values=None, index=None):
        self.name = name
        self.values = values
        self.index = index
        self.series = selector  # special series designator

    def getall(self):
        return Series(name=self.name, index=self.index, values=self.values)


def generate_dataframe(args=None):
    name = None
    index = None
    columns = None
    if hasattr(args, NAME_PROPERTY):
        name = copy(c_unbox(args.name))
    if hasattr(args, INDEX_PROPERTY):
        index = deepcopy(c_unbox(args.index))
    if hasattr(args, COLUMNS_PROPERTY):
        columns = deepcopy(c_unbox(args.columns))
    args.remove([NAME_PROPERTY, INDEX_PROPERTY, COLUMNS_PROPERTY])
    values = args.values()
    if isinstance(values, list):
        if len(values) == 1:
            values = values[0]
    keys = args.keys()
    if None not in keys:
        if columns is None:
            if len(keys) == len(values):
                values = args.dict()
    gen = DataframeGenerator(name=name, values=values, columns=columns, index=index)
    dframe = gen.getall()
    return dframe


def generate_dict(args=None):
    return None


def generate_list(args=None):
    return args.values()


def generate_set(args=None):
    return args.values()


def generate_tuple(args=None):
    return args.values()


def generate_named_tuple(args=None):
    return None


# UNDONE: right now we are materializing the generator product, but we could pass the generator back.
# UNDONE: just need to make sure that works in all cases.
def generate_range(args=None):
    start = end = _zero = 0
    step = 1
    args = list(filter(None.__ne__, args))
    ty = c_type(args[0])
    if ty == TK.STR:
        start = _parse_datetime(args[0])
        ty = TK.TIME
        if len(args) > 1:
            _e = args[1]
            if isinstance(_e, int):
                end = start + dt.timedelta(args[1])
            else:
                end = _parse_datetime(_e)
        if len(args) > 2:
            step = dt.timedelta(args[2])
        else:
            step = dt.timedelta(1)
    else:
        if ty == TK.DUR:
            step = dt.timedelta(days=1)
            _zero = dt.timedelta(days=0)
            start = end = _zero
        elif ty == TK.TIME:
            step = dt.timedelta(days=1)
            _zero = Time(dt.datetime.now())
            start = end = _zero
        elif ty not in [TK.INT, TK.FLOT]:
            raise TypeError(f"Unsupported range type TK.{TK(ty).name}")
        else:
            step = 1
        if len(args) == 1:
            end = args[0]
            if c_sign(end) < 0:
                start = args[0]
                end = _zero
        if len(args) > 1:
            start = args[0]
            end = args[1]
        if len(args) > 2:
            step = args[2]
    r = RangeGenerator(start=start, end=end, step=step)
    return r.getall()


def _parse_datetime(v):
    val = c_unbox(v)
    start = _parse_date_value(val, expect=False)
    if start is None:
        start = _parse_time_value(val, expect=False)
        if start is None:
            raise TypeError(f"{val} Does not represent a supported range type")
    return start


def generate_series(args=None):
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
