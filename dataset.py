from dataclasses import dataclass
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
