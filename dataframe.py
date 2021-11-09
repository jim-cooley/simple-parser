from dataclasses import dataclass
from scope import Object
import pandas as pd


@dataclass
class DataFrame(Object):
    """
    This class represents a Pandas DataFrame object.
    """
    def __init__(self, name=None, value=None, parent=None):
        super().__init__(name=name, token=None, value=value, parent=parent)
        self._dataframe = value or pd.DataFrame()

    def from_dataframe(self, df):
        pass
