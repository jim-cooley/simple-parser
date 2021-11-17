from enum import unique, IntEnum

from runtime.dataframe import create_dataset, create_series
from runtime.generators import generate_dataframe, generate_list, generate_series
from runtime.intrinsics import do_now
from runtime.print import do_print, init_print
from runtime.scope import IntrinsicFunction
from runtime.token_ids import TK
from runtime.yahoo import do_yahoo, init_yahoo


@unique
class SLOT(IntEnum):
    INVOKE = 0
    INIT = 1


def is_intrinsic(name):
    if name in _intrinsic_fundesc:
        return name
    return name in _instrinsic_aliases


def invoke_generator(env, name, args):
    return invoke_intrinsic(env, name, args, disptab=_generator_funcdesc)


def invoke_intrinsic(env, name, args, disptab=None):
    disptab = _intrinsic_fundesc if disptab is None else disptab
    if name.lower() in disptab:
        fn = disptab[name][SLOT.INVOKE]
    elif name.lower() in disptab:
        fn = disptab[name][SLOT.INVOKE]
    else:
        raise ValueError(f"Unknown function: {name}")
    if not args:
        return fn(env)
    else:
        return fn(env, args)


def init_intrinsic(name):
    if name.lower() in _intrinsic_fundesc:
        fn = _intrinsic_fundesc[name][SLOT.INIT]
        if fn is not None:
            return fn(name)
        else:
            return IntrinsicFunction(name=name)


# -----------------------------------
# Tables
# -----------------------------------

tk2generator = {
    TK.DATAFRAME: 'generate_dataframe',
    TK.LIST: 'generate_list',
    TK.SERIES: 'generate_series',
}


# these are function descriptors for the intrinsic functions
# the format is (invoke_fn, init_fn)
_intrinsic_fundesc = {
    'dataset': (create_dataset, None),
    'now': (do_now, None),
    'print': (do_print, init_print),
    'series': (create_series, None),
    'today': (do_now, None),
    'yahoo': (do_yahoo, init_yahoo),
}

# these are allowable aliases (which can easily be overridden)
_instrinsic_aliases = {
    'dataframe': (create_dataset, None),  # allowable for now
}

_generator_funcdesc = {
    'generate_dataframe': (generate_dataframe, None),
    'generate_list': (generate_list, None),
    'generate_series': (generate_series, None),
}


_intrinsic_not_impl = [
    # type constructors
    'Dataset',
    'dataset',
    "Series",
    "series",

    # functions (intrinsics)
    "ema",
    "sma",
    'columns',
    'fillempty',
    'select',
#   "signal",

    # NumPy
    'arrange',     # create array of evenly spaced values
    'corrcoef',    # correlation coefficient
    'cos',
    'cumsum',      # cummulative sum
    'dot',         # CONSIDER: turn this into operator ?
    'eye',         # create identity matrix
    'exp',
    'fill',        # create a constant array (np: full)
    'log',
    'linspace',    # create array of evenly spaced values (number of samples)
    'max',
    'mean',
    'median',
    'min',
    'ones',        # create an array of ones
    'random',      # create array of random values
    'rand',        # generate a random number (single sample)
    'std',         # standard deviation
    'sqrt',
    'sin',
    'sum',
    'zeros',       # create an array of zeros

    # Pandas
    'rank',        # assign ranks to entries

    # I/O
    'load',        # format=numpy will load numpy data, format=txt will save text. fomats to support: focal, numpy, pandas, excel, csv, text/other
    'save',        # format=numpy will save numpy data, format=txt will save text
]
