import pandas as pd


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
def pd_axes(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return df_axes(a)


def pd_index(args=None):
    return df_index(args[0])


def pd_info(args=None):
    return df_info(args[0])


def pd_values(args=None):
    return df_values(args[0])


def pd_boxplot(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    return pdi_boxplot(a)


def pdi_boxplot(a):
    plt.figure()
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


def pd_cumsum(args=None):
    a = args[0]
    if not isinstance(a, pd.DataFrame):
        a = pd.DataFrame(a)
    if len(args > 1):
        axis = args[1]
    else:
        axis = 'c'
    axis = axis[0].lower()
    return a.cumsum(axis=0 if axis == 'r' else 1)


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


def pd_head(args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_head(a, count)


def pdi_head(a, count):
    return a.head(count)


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
    return pdi_shift(a, delay)


def pdi_shift(a, delay):
    return a.shift(delay)


def do_signal(args=None):
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
    if len(args > 1):
        axis = args[1]
    else:
        axis = 'c'
    axis = axis[0].lower()
    return a.sum(axis=0 if axis == 'r' else 1)


def pd_tail(args=None):
    a = args[0]
    if len(args) > 1:
        count = args[1]
    else:
        count = 5  # pandas default
    return pdi_tail(a, count)


def pdi_tail(a, count):
    return a.tail(count)
