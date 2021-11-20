from enum import unique, IntEnum

from runtime.generators import generate_dataframe, generate_list, generate_series, generate_range
from runtime.intrinsics import do_now, create_dataset, create_series
from runtime.print import do_print, init_print
from runtime.scope import IntrinsicFunction
from runtime.token_ids import TK
from runtime.yahoo import do_yahoo, init_yahoo


@unique
class SLOT(IntEnum):
    INVOKE = 0
    ARGC = 1
    INIT = 2


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
        argc = disptab[name][SLOT.ARGC]
        if argc > 0:
            if not args:
                raise ValueError("Argument expected.")
            return fn(env, args)
        else:
            return fn(env)
    else:
        raise ValueError(f"Unknown function: {name}")


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
    TK.RANGE: 'generate_range',
    TK.SERIES: 'generate_series',
}


# these are function descriptors for the intrinsic functions
# the format is (invoke_fn, argc, init_fn)
_intrinsic_fundesc = {
    'dataset': (create_dataset, 1, None),
    'now': (do_now, 0, None),
    'print': (do_print, 1, init_print),  # varargs
    'range': (generate_range, 1, None),
    'series': (create_series, 1, None),
    'today': (do_now, 0, None),
    'yahoo': (do_yahoo, 1, init_yahoo),
}

# these are allowable aliases (which can easily be overridden)
_instrinsic_aliases = {
    'dataframe': (create_dataset, None),  # allowable for now
}

_generator_funcdesc = {
    'generate_dataframe': (generate_dataframe, 1, None),
    'generate_list': (generate_list, 1, None),
    'generate_range': (generate_range, 1, None),
    'generate_series': (generate_series, 1, None),
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
