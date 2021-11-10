import sys
from dataclasses import dataclass
from pandas.compat import numpy as np
from scope import Object
import pandas as pd


@dataclass
class Dataset(Object):
    """
    This class represents a Pandas DataFrame object.
    """
    def __init__(self, name=None, value=None, parent=None):
        super().__init__(name=name, token=None, value=value, parent=parent)
        self._dataframe = value or pd.DataFrame()

    def from_dataframe(self, df):
        pass


class Series(Object):
    """
    Pandas Series object
    """
    def __init__(self, name=None, value=None, parent=None):
        super().__init__(name=name, token=None, value=value, parent=parent)
        self._seroes = value or pd.Series()

    def from_series(self, df):
        pass


def create_dataset(args):
    d = Dataset()
    return d


def create_series(args):
    r = Series()
    return r


def set_print_options():
    np.set_printoptions(threshold=sys.maxsize)
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

