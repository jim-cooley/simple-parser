import numpy as np

from runtime.conversion import c_unbox, c_array_unbox


def np_zeros(env, args):
    npargs = c_array_unbox(args)
    if len(npargs) > 1:
        return np.zeros(tuple(npargs))
    return np.zeros(*npargs)


def np_ones(env, args):
    npargs = c_array_unbox(args)
    if len(npargs) > 1:
        return np.ones(tuple(npargs))
    return np.ones(*npargs)


def np_identity(env, args):
    npargs = c_array_unbox(args)
    return np.eye(*npargs)
