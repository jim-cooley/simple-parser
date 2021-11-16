from copy import copy, deepcopy

from runtime.conversion import c_unbox
from runtime.dataframe import Series

NAME_PROPERTY = 'name'
INDEX_PROPERTY = 'index'
COLUMNS_PROPERTY = 'columns'


def generate_dataframe(env, args):
    return None


def generate_list(env, args):
    return None


_DEFAULT_SERIES_ITEMS = {
    'name': None,
    'index': None,
}

_DEFAULT_DATAFRAME_ITEMS = {
    'name': None,
    'index': None,
    'columns': None,
}


def generate_series(env, args):
    name = None
    index = None
    if hasattr(args, NAME_PROPERTY):
        name = copy(c_unbox(args.name))
    if hasattr(args, INDEX_PROPERTY):
        index = deepcopy(c_unbox(args.index))
    args.remove([NAME_PROPERTY, INDEX_PROPERTY])
    series = Series(name=name, index=[name], values=args.dict())
    return series

