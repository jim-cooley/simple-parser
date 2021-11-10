from dataframe import create_dataset, create_series
from yahoo import do_yahoo


def is_intrinsic(name):
    return name in _intrinsic_dispatch


def invoke_intrinsic(name, args):
    if name.lower() in _intrinsic_dispatch:
        fn = _intrinsic_dispatch[name]
        return fn(args)


_intrinsic_dispatch = {
    'dataset': create_dataset,
    'series': create_series,
    'yahoo': do_yahoo,
}

