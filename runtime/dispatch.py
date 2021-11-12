from enum import unique, IntEnum

from runtime.dataframe import create_dataset, create_series
from runtime.intrinsics import do_now, do_print, init_print

from runtime.scope import IntrinsicFunction
from runtime.yahoo import do_yahoo, init_yahoo


@unique
class SLOT(IntEnum):
    INVOKE = 0
    INIT = 1


def is_intrinsic(name):
    if name in _intrinsic_fundesc:
        return name
    return name in _instrinsic_aliases


def invoke_intrinsic(env, name, args):
    if name.lower() in _intrinsic_fundesc:
        fn = _intrinsic_fundesc[name][SLOT.INVOKE]
    elif name.lower() in _instrinsic_aliases:
        fn = _instrinsic_aliases[name][SLOT.INVOKE]
    else:
        raise ValueError(f"Unknown function: {name}")
    if args is None or args.is_empty():
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

# these are allowable aliases (which can easily be overridden)
_instrinsic_aliases = {
    'dataframe': (create_dataset, None),  # allowable for now
}