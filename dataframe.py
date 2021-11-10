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

    # UNDONE: required elements for NumPy
    # .shape = array dimensions
    # len() = length of array
    # .ndim = number of array dimensions
    # .size = number of array elements
    # .dtype datatype of array elements
    # .dtype.name = name of the datatype
    # .astype(int) = convert an array to a different type

    # Pandas
    # apply()  - apply function to dataset - lambda functions
    # applymap - apply function elementwise (map function to dataset elements) - UNDONE: see about other lambda reductions
    # columns - describe columns
    # count - number of non NaN values
    # describe - elementary statistics
    # idxmin, idxmax = min/max index values
    # index - describe index
    # info - info on dataframe

    # NumPy functions:
    # .append
    # .column_stack = create stacked column-wise arrays
    # .concatenate
    # .delete
    # .hsplit = split the array horizontally -- look at slices for these
    # .hstack = horizontally stack arrays
    # .insert = insert items into the array
    # .ravel = flatten array
    # .reshape = reshape array
    # .resize
    # .sort(axis=) = sort the array by axis (or column/row?)
    # .transpose
    # .vsplit = split the array vertically
    # .vstack = vertically stack arrays together

    # comparison:
    # ==
    # <

    # slicing:
    # [0:2]         - range subset
    # [:2]  [1:]    - row / col select
    # [a<2]         - boolean indexing (select)
    # ['a']         - column 'a'

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

