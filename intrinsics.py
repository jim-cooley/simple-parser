from dataset import create_dataset, create_series


def is_intrinsic(name):
    return name in _intrinsic_dispatch


def invoke_intrinsic(name, args):
    if name.lower() in _intrinsic_dispatch:
        fn = _intrinsic_dispatch[name]
        return fn(args)


_intrinsic_dispatch = {
    'dataset': create_dataset,
    'series': create_series,
}

