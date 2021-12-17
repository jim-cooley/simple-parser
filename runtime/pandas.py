import math

import numpy as np
import pandas as pd
import datetime as dt

from runtime.conversion import c_unbox
from runtime.indexdict import IndexedDict
from runtime.series import Series


def set_print_options(options=None):
    if options is None:
        return set_print_options_truncated()
    elif options.full:
        return set_print_options_full()
    else:
        return pd.option_context(
            'display.max_rows', options.max_rows,
            'display.max_columns', options.max_columns,
            'display.width', options.width,
        )


def set_print_options_full():
    return pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 16384,
    )


def set_print_options_truncated():
    return pd.option_context(
        'display.max_rows', 20,
        'display.max_columns', 20,
        'display.width', 256,
    )


def print_dataframe(_df, options=None, label=None):
    _df = c_unbox(_df)
    with set_print_options(options):
        if label:
            print(label)
        print(_df)


def print_series(_s, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_s)


def create_dataset(args=None):
    if len(args) > 0:
        return pd.DataFrame(args[0])
    return pd.DataFrame()


def create_series(args=None):
    r = Series()
    return r


# -----------------------------------
# DataFrame methods
# -----------------------------------
def df_set_at(df, index, value):
    if isinstance(index, list):
        index = index[0]
    df[index] = value


def df_axes(df=None):
    return df.axes


def df_clip(df, args=None):
    lower = upper = None
    if len(args) == 1:
        upper = args[0]
    if len(args) == 2:
        lower = args[0]
        upper = args[1]
    return df.clip(lower=lower, upper=upper)


def df_columns(a, columns=None):
    if columns:
        if isinstance(columns, IndexedDict):
            columns = columns.values()
        return a[columns]
    return a.columns.values


def df_set_columns(a, columns):
    if columns:
        a.columns = columns


def df_set_idx_columns(a, index, value):
    if value:
        a.columns[index] = value


# is_empty
def df_empty(df=None):
    return df.empty


def df_set_flags(args=None):
    pass


def df_head(df, args):
    return df.head(args[0])


def df_index(df=None):
    return df.index.values


def df_info(df=None):
    return df.info


def df_shape(df=None):
    return df.shape


def df_values(df=None):
    return df.values


# -----------------------------------
# Pandas Binops
# -----------------------------------
def _slice_dataframe(l_value, r_value):
    stop = step = None
    start = r_value[0]
    if len(r_value) > 1:
        stop = r_value[1]
    if len(r_value) > 2:
        step = r_value[2]
    return l_value[slice(start, stop, step)]


def _slice_series(l_value, r_value):
    stop = step = None
    start = r_value[0]
    if len(r_value) > 1:
        stop = r_value[1]
    if len(r_value) > 2:
        step = r_value[2]
    return l_value[slice(start, stop, step)]


def df_negate(df):
    return df * -1


def pd_and_df(a, b):
    return pdi_intersection(a, b)


def pd_or_df(a, b):
    return pdi_union(a, b)


def pd_eq_df(a, b):
    return a == b


def pd_neq_df(a, b):
    return a != b


def pd_gtr_df(a, b):
    return a > b


def pd_gte_df(a, b):
    return a >= b


def pd_less_df(a, b):
    return a < b


def pd_lte_df(a, b):
    return a <= b


def pd_mul_df(a, b):
    return a * b


def pdi_union(df, other):
    return df.combine(other, s_union, fill_value=None, overwrite=False)


def s_union(s1, s2):
    return s1.combine(s2, lambda e1, e2: e2 if e1 is None else e1, fill_value=None)


def pdi_intersection(df, other):
    return df.combine(other, s_intersection, fill_value=None, overwrite=False)


def s_intersection(s1, s2):
    return s1.combine(s2, lambda ele1, ele2: ele1 if ele1 == ele2 else None, fill_value=None)


# -----------------------------------
# Pandas Functions
# -----------------------------------
def pd_axes(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return df_axes(a)


def pd_boxplot(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_boxplot(a)


def pdi_boxplot(a):
    # plt.figure()
    boxplot = a.boxplot()
    return boxplot


def pd_columns(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if len(args) > 1:
        columns = args.values()[1:]
    else:
        columns = None
    return df_columns(a, columns)


def pd_clipbefore(args=None):
    df = args[0]
    before = args[1]
    lower = upper = fillna = None
    if len(args) == 3:
        upper = args[2]
    if len(args) >= 4:
        lower = args[2]
        upper = args[3]
    if len(args) == 5:
        fillna = args[4]
    return df.transform(si_clipfunc, before=before, upper=upper, lower=lower, fillna=fillna)


def si_clipfunc(series, before=None, upper=None, lower=None, fillna=None):
    s = series.copy()
    for idx in series.index:
        item = series[idx]
        if before is not None:
            if item != before:
                item = upper if item > upper else item
                item = lower if item < lower else item
            else:
                before = None
        if fillna is not None:
            if np.isnan(item):
                item = fillna
        s[idx] = item
    return s


def pd_clip(args=None):
    df = args[0]
    lower = upper = None
    if len(args) == 2:
        upper = args[1]
    if len(args) == 3:
        lower = args[1]
        upper = args[2]
    return df.clip(lower=lower, upper=upper)


def pd_combine(args=None):
    df = args[0]
    other = args[1]
    return pdi_union(df, other)


def pd_cumsum(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if len(args) > 1:
        axis = args[1]
    else:
        axis = 'c'
    axis = axis[0].lower()
    return a.cumsum(axis=1 if axis == 'r' else 0)


def pd_delta(args=None):
    a = args[0]
    if len(args) > 1:
        delay = args[1]
    else:
        delay = 1
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_delta(a, delay)


def pdi_delta(a, delay):
    if delay == 1:
        return a.diff()
    return a - a.shift(delay)


def pd_describe(args=None):
    cols = pctile = None
    a = args[0]
    if len(args) > 1:
        cols = args[1]
    if len(args) > 2:
        pctile = args[2]
    if isinstance(a, pd.DataFrame) or isinstance(a, pd.Series):
        return a.describe(include=cols, percentiles=pctile, datetime_is_numeric=True)
    return None


def pd_head(args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_head(a, count)


def pdi_head(a, count):
    return a.head(count)


def pd_index(args=None):
    return df_index(args[0])


def pd_info(args=None):
    return df_info(args[0])


def pd_shape(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        raise TypeError('Object is not a DataFrame')
    return a.shape


def pd_shift(args=None):
    a = args[0]
    delay = args[1]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if isinstance(delay, dt.timedelta):
        delay = delay // dt.timedelta(days=1)
    return pdi_shift(a, delay)


def pdi_shift(a, delay):
    return a.shift(delay).fillna(0)


def do_signal(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return di_signal(a)


def di_signal(a):
    series = a.fillna(0)
    series[series > 0] = 1
    series[series < 1] = 0
    signal = series.diff()
    return signal


def pd_sma(args=None):
    a = args[0]
    window = args[1]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_sma(a, window)


def pdi_sma(a, window):
    return a.rolling(window).mean()


def pd_sum(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if len(args) > 1:
        axis = args[1]
    else:
        axis = 'c'
    axis = axis[0].lower()
    return a.sum(axis=1 if axis == 'r' else 0)


def pd_tail(args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_tail(a, count)


def pdi_tail(a, count):
    return a.tail(count)


def pd_trim(args=None):
    axis = 'c'
    uval = []
    df = args[0]
    if len(args) > 1:
        uval = args[1]
    values = [None, np.NaN].append(uval)
    return pdi_trim(df, axis, values)


def pdi_trim(df, axis, values):
    first = df.first_valid_index()
    last = df.last_valid_index()
    if first is not None:
        df = df.truncate(axis='index', before=first)
    if last is not None:
        df = df.truncate(axis='index', after=last)
    return df


def pd_values(args=None):
    return df_values(args[0])
