import pandas as pd
import matplotlib.pyplot as plt


from runtime.conversion import c_unbox
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


def create_dataset(env=None, args=None):
    if len(args) > 0:
        return pd.DataFrame(args[0])
    return pd.DataFrame()


def create_series(env=None, args=None):
    r = Series()
    return r


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


def pd_and_df(a, b):
    return a and b


def pd_or_df(a, b):
    return a or b


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


# -----------------------------------
# Pandas Functions
# -----------------------------------
def pd_boxplot(env=None, args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_boxplot(a)


def pdi_boxplot(a):
    plt.figure()
    boxplot = a.boxplot()
    return boxplot


def pd_columns(env=None, args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if len(args) > 1:
        columns = args.values()[1:]
    else:
        columns = None
    return pdi_columns(a, columns)


def pdi_columns(a, columns):
    if columns:
        return a[columns]
    return a


def pd_delta(env=None, args=None):
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


def pd_head(env=None, args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_head(a, count)


def pdi_head(a, count):
    return a.head(count)


def pd_shift(env=None, args=None):
    a = args[0]
    delay = args[1]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_shift(a, delay)


def pdi_shift(a, delay):
    return a.shift(delay)


def do_signal(env=None, args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return di_signal(a)


def di_signal(a):
    series = a.fillna(0)
    series[series > 0] = 1
    series[series < 1] = 0
    signal = series.diff().fillna(0)
    return signal


def pd_sma(env=None, args=None):
    a = args[0]
    window = args[1]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_sma(a, window)


def pdi_sma(a, window):
    return a.rolling(window).mean()


def pd_tail(env=None, args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_tail(a, count)


def pdi_tail(a, count):
    return a.tail(count)
