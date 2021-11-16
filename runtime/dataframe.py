from copy import deepcopy
from dataclasses import dataclass

from runtime.indexdict import IndexedDict
from runtime.scope import Object
import pandas as pd

from runtime.token import Token


@dataclass
class Dataset(Object):
    """
    This class represents a Pandas DataFrame object.
    """
    def __init__(self, name=None, value=None, parent=None, loc=None):
        super().__init__(name=name, value=value, parent=parent, token=Token.DATAFRAME(loc=loc))
        self._dataframe = value if value is not None else pd.DataFrame()
        if isinstance(value, dict) or isinstance(value, IndexedDict):
            self._dataframe = pd.DataFrame(value, columns=list(value.keys()), index=[''])
        elif type(self._dataframe).__name__ != 'DataFrame':
            raise ValueError("object is not DataFrame")
        self._value = self._dataframe
        self._items = []

    def items(self):
        """
        items is a list of AST 'items' used to construct this dataframe instance.
        """
        return self._items

    def values(self):
        """
        Values is the Dataframe data values themselves
        """
        return self._value

    def from_dict(self, other):
        pass

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
    def __init__(self, name=None, values=None, index=None, parent=None, loc=None):
        super().__init__(name=name, value=values, parent=parent, token=Token.SERIES(loc=loc))
        if values is not None:
            self._value = pd.Series(name=name, data=values, index=index)  # UNDONE: defer construction
        else:
            self._value = pd.Series()

    def values(self):
        """
        Values is the Series data values themselves
        """
        return self._value

    def from_dict(self, other):
        pass

    def from_series(self, series):
        self._value = deepcopy(series)

    def series(self):
        return self._series

    def dict(self):
        pass

    # UNDONE: copies List() for now
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
                fstr = f'count={len(self._value)-1}'
            return '[' + f'{fstr}' + ']'

    def print(self):
        print_series(self._value)


def create_dataset(args):
    d = Dataset()
    return d


def create_series(args):
    r = Series()
    return r


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


def set_print_options():
#   np.set_printoptions(threshold=sys.maxsize)
    return pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 16384,
    )