import pandas as pd

from runtime.dataframe import Dataset
from runtime.series import Series


def set_print_options():
    return pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 16384,
    )


def print_dataframe(_df, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_df)


def print_series(_s, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_s)


def create_dataset(env=None, args=None):
    d = Dataset()
    return d


def create_series(env=None, args=None):
    r = Series()
    return r
