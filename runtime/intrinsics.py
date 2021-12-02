from dataclasses import dataclass
from enum import unique, IntEnum

from runtime.generators import generate_range, generate_dataframe, generate_dict, generate_list, generate_named_tuple, \
    generate_series, generate_set, generate_tuple
from runtime.numpy import np_identity, np_ones, np_zeros
from runtime.pandas import create_dataset, create_series
from runtime.print import do_print, init_print
from runtime.scope import FunctionBase
from runtime.time import do_now
from runtime.token_ids import TK
from runtime.yahoo import do_yahoo, init_yahoo


@unique
class SLOT(IntEnum):
    INVOKE = 0
    ARITY = 1
    INIT = 2


@dataclass
class IntrinsicFunction(FunctionBase):
    def __init__(self, name=None, members=None, arity=None, defaults=None, tid=None, loc=None, is_lvalue=False):
        super().__init__(name=name, members=members, defaults=defaults, tid=tid, loc=loc, is_lvalue=is_lvalue)
        self.token.is_reserved = True

    def invoke(self, interpreter, args=None):
        result = invoke_intrinsic(env=interpreter.environment, name=self._name, args=args)
        interpreter.stack.push(result)


def is_intrinsic(name):
    if name in _intrinsic_fundesc:
        return name
    return name in _intrinsic_aliases


def invoke_intrinsic(env, name, args, disptab=None, locator=None):
    return invoke_intrinsic_internal(env, name, args, locator='intrinsic')


def invoke_generator(env, name, args):
    return invoke_intrinsic_internal(env, name, args, locator='generator')


def invoke_intrinsic_internal(env, name, args, locator=None):
    locator = locator or 'intrinsics'
    disptab = _funcdesc_locator[locator][0]
    aliases = _funcdesc_locator[locator][1]
    if aliases is not None:
        if name.lower() in aliases:
            name = aliases[name.lower()]
    if name.lower() in disptab:
        fn = disptab[name][SLOT.INVOKE]
        arity = disptab[name][SLOT.ARITY]
        if arity > 0:
            if not args:
                raise ValueError("Argument expected.")
            return fn(env, args)
        else:
            return fn(env)
    else:
        raise ValueError(f"Unknown function: {name}")


def load_intrinsics(intrinsics=None):
    fndesc = {}
    intrinsics = intrinsics or _intrinsic_fundesc
    for fname, desc in intrinsics.items():
        fn = init_intrinsic(fname)
        fndesc[fname] = fn
    return fndesc


def load_intrinsics_not_impl(not_impl=None):
    fndesc = {}
    not_impl = not_impl or _intrinsic_not_impl
    for fname, desc in not_impl.items():
        fn = IntrinsicFunction(name=fname, arity=desc[SLOT.ARITY], tid=TK.IDENT)
        fndesc[fname] = fn
    return fndesc


def init_intrinsic(name):
    if name.lower() in _intrinsic_fundesc:
        desc = _intrinsic_fundesc[name]
        fn = desc[SLOT.INIT]
        if fn is not None:
            return IntrinsicFunction(name=name, defaults=fn(name))
        else:
            return IntrinsicFunction(name=name, arity=desc[SLOT.ARITY])


# -----------------------------------
# Intrinsic Init Functions
# -----------------------------------
_intrinsic_aliases = {
    'dataframe': 'dataset',
    'eye': 'identity',
}


# -----------------------------------
# Intrinsic Function Descriptors
# -----------------------------------
# format is: do_ is called by Invoke and handles any parameter validation / massaging.
#            init_ is called by keword_init to load the function descriptors and default parameters
#            get_ is used by internal functions to retrieve the results of the intrinsic without the parameter
#                 manipulation and will be called with native types as input.  Internal types are returned by convention

_intrinsic_fundesc = {
    # name     ( do_func, arity, init_func )
    'dataset': (create_dataset, 1, None),
    'identity': (np_identity, 1, None),
    'now': (do_now, 0, None),
    'ones': (np_ones, 1, None),
    'print': (do_print, 1, init_print),  # varargs
    'range': (generate_range, 1, None),
    'series': (create_series, 1, None),
    'today': (do_now, 0, None),
    'yahoo': (do_yahoo, 1, init_yahoo),
    'zeros': (np_zeros, 1, None),
}
_intrinsic_not_impl = {
    # type constructors
    'Dataset': (None, 0, None),
    'dataset': (None, 0, None),
    "Series": (None, 0, None),
    "series": (None, 0, None),

    # functions (intrinsics)
    "ema": (None, 1, None),
    "sma": (None, 1, None),
    'columns': (None, 0, None),
    'fillempty': (None, 0, None),
    'select': (None, 0, None),

    # NumPy
    'arrange': (None, 0, None),     # create array of evenly spaced values
    'corrcoef': (None, 0, None),    # correlation coefficient
    'cos': (None, 0, None),
    'cumsum': (None, 0, None),      # cummulative sum
    'dot': (None, 0, None),         # CONSIDER: turn this into operator ?
    'exp': (None, 0, None),
    'fill': (None, 0, None),        # create a constant array (np: full)
    'log': (None, 0, None),
    'linspace': (None, 0, None),    # create array of evenly spaced values (number of samples)
    'max': (None, 0, None),
    'mean': (None, 0, None),
    'median': (None, 0, None),
    'min': (None, 0, None),
    'random': (None, 0, None),      # create array of random values
    'rand': (None, 0, None),        # generate a random number (single sample)
    'std': (None, 0, None),         # standard deviation
    'sqrt': (None, 0, None),
    'sin': (None, 0, None),
    'sum': (None, 0, None),

    # Pandas
    'rank': (None, 0, None),        # assign ranks to entries

    # I/O
    'load': (None, 0, None),        # format=numpy will load numpy data, format=txt will save text. fomats to support: focal, numpy, pandas, excel, csv, text/other
    'save': (None, 0, None),        # format=numpy will save numpy data, format=txt will save text
}
_generator_funcdesc = {
    'generate_dataframe': (generate_dataframe, 1, None),
    'generate_dict': (generate_dict, 1, None),
    'generate_list': (generate_list, 1, None),
    'generate_named_tuple': (generate_named_tuple, 1, None),
    'generate_range': (generate_range, 1, None),
    'generate_series': (generate_series, 1, None),
    'generate_set': (generate_set, 1, None),
    'generate_tuple': (generate_tuple, 1, None),
}
tk2generator = {
    TK.DATAFRAME: 'generate_dataframe',
    TK.DICT: 'generate_dict',
    TK.LIST: 'generate_list',
    TK.NAMEDTUPLE: 'generate_named_tuple',
    TK.RANGE: 'generate_range',
    TK.SERIES: 'generate_series',
    TK.SET: 'generate_set',
    TK.TUPLE: 'generate_tuple',
}
_funcdesc_locator = {
    'intrinsic': (_intrinsic_fundesc, _intrinsic_aliases),
    'generator': (_generator_funcdesc, None),
}
