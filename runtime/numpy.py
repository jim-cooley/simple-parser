import numpy as np

from runtime.conversion import c_unbox, c_array_unbox


def _slice_ndarray(l_value, r_value):
    stop = step = None
    start = r_value[0]
    if len(r_value) > 1:
        stop = r_value[1]
    if len(r_value) > 2:
        step = r_value[2]
    return l_value[slice(start, stop, step)]


def np_fill(env, args):
    a = args[0]
    if isinstance(a, np.ndarray):
        val = args[1]
    else:
        val = args[0]
        x = args[1]
        y = args[2]
        a = np.ndarray((x, y))
    return a.fill(val)


def np_flatten(env, args):
    a = args[0]
    if not isinstance(a, np.ndarray):
        a = np.ndarray(a)
    return a.flatten(order='C')


def np_identity(env, args):
    npargs = c_array_unbox(args)
    return np.eye(*npargs)


def np_integers(env, args):
    argc = len(args)
    rng = np.random.default_rng()
    if isinstance(args[0], list):
        l = args[0]
        low = l[0]
        high = l[-1]
        if argc == 1:
            return rng.integers(low, high)
        elif argc == 2:
            return rng.integers(low, high, (args[1],))
        elif argc == 3:
            x = args[1]
            y = args[2]
            return rng.integers(low, high, (x, y))
        else:
            x = args[1]
            y = args[2]
            z = args[3]
            return rng.integers(low, high, (x, y, z))
    else:
        if argc == 1:
            high = args[0]
            low = 0
            x = y = 1
        elif argc == 2:
            x = args[0]
            y = args[1]
            low = 0
            high = 2
        elif argc == 3:
            high = args[0]
            low = 0
            x = args[1]
            y = args[2]
        else:
            high = args[0]
            low = args[1]
            x = args[2]
            y = args[3]
    if argc < 4:
        return rng.integers(low, high, size=(x, y))
    else:
        z = args[4]
        return rng.integers(low, high, size=(x, y, z))


def np_ones(env, args):
    npargs = c_array_unbox(args)
    if len(npargs) > 1:
        return np.ones(tuple(npargs))
    return np.ones(*npargs)


def np_random(env, args):
    argc = len(args)
    rng = np.random.default_rng()
    if argc == 0:
        return rng.random()
    elif argc == 1:
        size = args[0]
        return rng.random((size,))
    elif argc == 2:
        x = args[0]
        y = args[1]
        return rng.random((x, y))
    elif argc == 3:
        x = args[0]
        y = args[1]
        z = args[2]
        return rng.random((x, y, z))


def np_reshape(env, args):
    a = args[0]
    x = args[1]
    if len(args) > 2:
        y = args[2]
        return np.reshape(a, (x, y), 'A')
    else:
        assert x == -1, "only 1D given and not flatten"
        return np.reshape(a, x, 'A')    # x == -1 is flatten.


def np_shape(env, args):
    a = args[0]
    return np.shape(a)


def np_transpose(env, args):
    a = args[0]
    if not isinstance(a, np.ndarray):
        a = np.ndarray(a)
    return np.transpose(a)


def np_zeros(env, args):
    npargs = c_array_unbox(args)
    if len(npargs) > 1:
        return np.zeros(tuple(npargs))
    return np.zeros(*npargs)


