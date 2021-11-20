from copy import deepcopy

import pandas as pd

from runtime.pandas import print_series
from runtime.scope import Object
from runtime.token import Token


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
