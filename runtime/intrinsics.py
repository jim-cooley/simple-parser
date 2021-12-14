from dataclasses import dataclass
from enum import unique, IntEnum

import numpy as np
import pandas as pd
import json as js

from runtime.conversion import c_unbox
from runtime.generators import generate_range, generate_dataframe, generate_dict, generate_list, generate_named_tuple, \
    generate_series, generate_set, generate_tuple
from runtime.numpy import np_identity, np_ones, np_zeros, np_reshape, np_flatten, np_transpose, np_random, \
    np_integers, np_fill
from runtime.pandas import create_dataset, create_series, pd_sma, pd_columns, pd_shift, pd_delta, do_signal, pd_head, \
    pd_tail, pd_boxplot, pd_values, pd_index, pd_info, pd_axes, pd_sum, pd_cumsum
from runtime.print import do_print
from runtime.scope import FunctionBase
from runtime.time import do_now
from runtime.token_ids import TK
from runtime.yahoo import do_yahoo, init_yahoo


@unique
class SLOT(IntEnum):
    INVOKE = 0
    ARITY = 1
    MAX = 2
    INIT = 3


@dataclass
class IntrinsicFunction(FunctionBase):
    def __init__(self, name=None, members=None, closure=None, arity=None, opt=None, invoke=None, defaults=None, tid=None, loc=None, is_lvalue=False):
        super().__init__(name=name, members=members, closure=closure, arity=arity, opt=opt,
                         defaults=defaults, tid=tid, loc=loc, is_lvalue=is_lvalue)
        self.token.is_reserved = True
        self._invoke_fn = invoke

    def invoke(self, interpreter, args=None):
        return self._invoke_fn(args=args)


@dataclass
class GeneratorFunction(IntrinsicFunction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def invoke(self, interpreter, args=None):
        return self._invoke_fn(args=args)


@dataclass
class IntrinsicNotImplemented(IntrinsicFunction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def invoke(self, interpreter, args=None):
        assert False, f'Function {self.name} is not implemented'


def is_intrinsic(name):
    if name in _intrinsic_fundesc:
        return name
    return name in _intrinsic_aliases


def invoke_generator(name, args):
    return invoke_intrinsic_internal(name, args, locator='generator')


def invoke_intrinsic_internal(name, args, locator=None):
    locator = locator or 'intrinsics'
    disptab = _funcdesc_locator[locator][0]
    aliases = _funcdesc_locator[locator][1]
    if aliases is not None:
        if name.lower() in aliases:
            name = aliases[name.lower()]
    if name.lower() in disptab:
        fn = disptab[name][SLOT.INVOKE]
        arity = disptab[name][SLOT.ARITY]
        cmax = disptab[name][SLOT.MAX]
        if cmax == 0:
            return fn()
        else:
            if arity and not args:
                raise ValueError("Argument expected.")
            if cmax > 0:
                if len(args) > cmax:
                    raise ValueError("Argument count mismatch.")
            return fn(args)
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
        fn = IntrinsicNotImplemented(name=fname, arity=desc[SLOT.ARITY], tid=TK.IDENT)
        fndesc[fname] = fn
    return fndesc


def init_intrinsic(name):
    if name.lower() in _intrinsic_fundesc:
        desc = _intrinsic_fundesc[name]
        invoke_fn = desc[SLOT.INVOKE]
        init_fn = desc[SLOT.INIT]
        if init_fn is not None:
            if isinstance(init_fn, dict):
                defaults = init_fn
            elif isinstance(init_fn, list):
                defaults = {k: None for k in init_fn}
            else:
                defaults = init_fn(name)
            return IntrinsicFunction(name=name, invoke=invoke_fn,
                                     arity=desc[SLOT.ARITY], opt=desc[SLOT.MAX], defaults=defaults)
        else:
            return IntrinsicFunction(name=name, invoke=invoke_fn, arity=desc[SLOT.ARITY], opt=desc[SLOT.MAX])


# -----------------------------------
# Intrinsic Functions
# -----------------------------------
def do_len(args=None):
    o = args[0]
    return len(o)


def to_json(args=None):
    fname = json = None
    o = args[0]
    if len(args) > 1:
        fname = args[1]
    if isinstance(o, pd.DataFrame):
        if fname is not None:
            with open(fname, 'w') as file:
                json = pd.io.json.to_json(file, o)
        else:
            json = pd.io.json.to_json(None, o)
        return json
    else:
        json = js.dumps(o)
        if fname is not None:
            with open(fname, 'w') as file:
                file.write(json)
    return json


def do_read(args=None):
    format = 'csv'
    dframe = None
    fname = args[0]
    if hasattr(args, 'format'):
        format = args.format
    if format == 'excel':
        dframe = pd.read_excel(fname)
    else:
        with open(fname, 'r') as file:
            if format == 'csv':
                dframe = pd.read_csv(file, header=0, index_col=0)
            elif format == 'json':
                dframe = pd.read_json(file)
            elif format == 'latex':
                dframe = pd.read_latex(file)
            elif format == 'pickle':
                dframe = pd.read_pickle(fname)
            elif format == 'table':
                dframe = pd.read_table(file)
            elif format == 'xml':
                dframe = pd.read_xml(file)
    return dframe


def do_shape(args=None):
    o = args[0]
    if isinstance(o, np.ndarray):
        np.shape(o)
    if isinstance(o, pd.DataFrame):
        return o.shape
    return len(o)


def do_typeof(args=None):
    o = args[0]
    return type(o).__name__


def do_write(args=None):
    format = 'csv'
    o = c_unbox(args[0])
    fname = args[1]
    if hasattr(args, 'format'):
        format = args.format
    if format == 'excel':
        o.to_excel(pd.ExcelWriter(fname))
    elif format == 'pickle':
        o.to_pickle(fname)
    else:
        with open(fname, 'w') as file:
            if isinstance(o, pd.DataFrame):
                if format == 'json':
                    o.to_json(file)
                elif format == 'csv':
                    o.to_csv(file)
                elif format == 'xml':
                    o.to_xml(file)
                elif format == 'latex':
                    o.to_latex(file)


# -----------------------------------
# Intrinsic Function Descriptors
# -----------------------------------
# format is: do_ is called by Invoke and handles any parameter validation / massaging.
#            init_ is called by keword_init to load the function descriptors and default parameters
#            get_ is used by internal functions to retrieve the results of the intrinsic without the parameter
#                 manipulation and will be called with native types as input.  Internal types are returned by convention

_intrinsic_fundesc = {
    # name     ( do_func, arity, opt, init_func )
    'columns': (pd_columns, 1, -1, None),
    'dataset': (create_dataset, 0, 1, None),
    'dataframe': (create_dataset, 0, 1, None),
    'delay': (pd_shift, 2, 2, None),    # alias for pandas 'shift'
    'delta': (pd_delta, 1, 2, None),    # focal
    'len': (do_len, 1, 1, None),
    'json': (to_json, 1, 2, None),   # obj [, filename]
    'now': (do_now, 0, 0, None),
    'print': (do_print, 1, -1, None),  # varargs
    'range': (generate_range, 1, 3, {'start': None, 'end': None, 'step': 1}),
    'read': (do_read, 1, 2, None),
    'series': (create_series, 0, 1, None),
    'signal': (do_signal, 1, 1, None),
    'today': (do_now, 0, 0, None),
    'type': (do_typeof, 1, 1, None),
    'write': (do_write, 1, 2, None),
    'yahoo': (do_yahoo, 1, 7, init_yahoo),

    # numpy:
    'eye': (np_identity, 1, 1, None),
    'fill': (np_fill, 2, 3, None),
    'flatten': (np_flatten, 1, 1, None),
    'identity': (np_identity, 1, 1, None),
    'integers': (np_integers, 0, 4, None),
    'ones': (np_ones, 1, 3, None),
    'random': (np_random, 1, 4, None),
    'reshape': (np_reshape, 2, 3, None),
    'shape': (do_shape, 1, 1, None),
    'transpose': (np_transpose, 1, 1, None),
    'zeros': (np_zeros, 1, 3, None),

    # pandas:
    'axes': (pd_axes, 1, 1, None),
    'boxplot': (pd_boxplot, 1, 4, None),
    'cumsum': (pd_cumsum, 1, 2, None),
    'head': (pd_head, 1, 2, None),
    'info': (pd_info, 1, 1, None),
    'index': (pd_index, 1, 1, None),
    'shift': (pd_shift, 2, 2, None),
    'sma': (pd_sma, 2, 2, None),
    'sum': (pd_sum, 1, 2, None),
    'tail': (pd_tail, 1, 2, None),
    'values': (pd_values, 1, 2, None),
    # timedelta_range
}

_intrinsic_aliases = {
    'dataframe': 'dataset',
    'eye': 'identity',
    'ident': 'identity',
}

_intrinsic_not_impl = {
    # functions (intrinsics)
    "ema": (None, 1, 1, None),
    'select': (None, 0, 1, None),

    # NumPy
    'arrange': (None, 0, 1, None),     # create array of evenly spaced values
    'corrcoef': (None, 0, 1, None),    # correlation coefficient
    'cos': (None, 0, 1, None),
    'cumsum': (None, 0, 1, None),      # cummulative sum
    'dot': (None, 0, 1, None),         # CONSIDER: turn this into operator ?
    'exp': (None, 0, 1, None),
    'log': (None, 0, 1, None),
    'linspace': (None, 0, 1, None),    # create array of evenly spaced values (number of samples)
    'max': (None, 0, 1, None),
    'mean': (None, 0, 1, None),
    'median': (None, 0, 1, None),
    'min': (None, 0, 1, None),
    'rand': (None, 0, 1, None),        # generate a random number (single sample)
    'std': (None, 0, 1, None),         # standard deviation
    'sqrt': (None, 0, 1, None),
    'sin': (None, 0, 1, None),
    'sum': (None, 0, 1, None),

    # Pandas
    'rank': (None, 0, 1, None),        # assign ranks to entries
    'fillempty': (None, 0, 1, None),
    'date_range': (None, 0, 1, None),  # would be nice to build a DateRange Generator

    # I/O
    'load': (None, 0, 1, None),        # format=numpy will load numpy data, format=txt will save text. fomats to support: focal, numpy, pandas, excel, csv, text/other
    'save': (None, 0, 1, None),        # format=numpy will save numpy data, format=txt will save text
}
_generator_funcdesc = {
    'generate_dataframe': (generate_dataframe, 1, -1, None),
    'generate_dict': (generate_dict, 1, -1, None),
    'generate_list': (generate_list, 1, -1, None),
    'generate_named_tuple': (generate_named_tuple, 1, -1, None),
    'generate_range': (generate_range, 1, -1, None),
    'generate_series': (generate_series, 1, -1, None),
    'generate_set': (generate_set, 1, -1, None),
    'generate_tuple': (generate_tuple, 1, -1, None),
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
