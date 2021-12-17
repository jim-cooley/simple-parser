from enum import unique, IntEnum

from runtime.pandas import df_index, df_columns, df_axes, df_empty, df_info, df_set_flags, df_shape, df_values, \
    df_set_columns, df_head, df_set_idx_columns, df_set_at, pd_trim, df_clip
from runtime.scope import Object

# instead of using distinct types for each native type, we use a generic 'object' as a container
# and use a 'descriptor' object for the method implementations.  This is 'shadowed' behind the object
# of interest in the scope resolution chain when evaluating propref's

# python binding:
# a.x => type(a).__dict__['x'].__get__(a, type(a))  # instance binding
# A.x => A.__dict__['x'].__get__(None, A)           # class binding
#

_NOT_INITED = True


@unique
class SLOT(IntEnum):
    INVOKE = 0
    GET = 1
    PUT = 2
    GETAT = 3
    PUTAT = 4


class Descriptor:
    def __init__(self, ty=None, members=None):
        self.type = ty
        self.members = members or {}

    def get(self, obj, prop):
        if prop in self.members:
            if hasattr(obj, 'value'):
                obj = obj.value
            fn = self.members[prop][SLOT.GET]
            if fn is None:
                assert False, f"invalid operation 'get' called on property {prop}"
            return fn(obj)
        elif hasattr(obj, prop):
            return getattr(obj, prop, None)
        elif hasattr(obj, 'value'):
            val = obj.value
            if hasattr(val, prop):
                return getattr(val, prop, None)
        assert False, f"property {prop} undefined"

    def set(self, obj, prop, value):
        if prop in self.members:
            if hasattr(obj, 'value'):
                obj = obj.value
            fn = self.members[prop][SLOT.PUT]
            if fn is not None:
                fn(obj, value)
            else:
                assert False, f"invalid operation 'set' called on property {prop}"
        elif hasattr(obj, prop):
            setattr(obj, prop, value)
        elif hasattr(obj, 'value'):
            val = obj.value
            if hasattr(val, prop):
                setattr(val, prop, value)
        else:
            assert False, f"property {prop} undefined"

    def getAt(self, obj, index, prop):
        if prop in self.members:
            if hasattr(obj, 'value'):
                obj = obj.value
            fn = self.members[prop][SLOT.GETAT]
            if fn is None:
                assert False, f"invalid operation 'getidx' called on property {prop}"
            return fn(obj, index)
        assert False, f"property {prop} undefined"

    def setAt(self, obj, prop, index, value):
        if prop is None:
            prop = '_'
        if prop in self.members:
            if hasattr(obj, 'value'):
                obj = obj.value
            fn = self.members[prop][SLOT.PUTAT]
            if fn is None:
                assert False, f"invalid operation 'setAt' called on property {prop}"
            fn(obj, index, value)
        else:
            assert False, f"property {prop} undefined"

    def invoke(self, obj, method, args):
        if method in self.members:
            fn = self.members[method][SLOT.INVOKE]
            if hasattr(obj, 'value'):
                obj = obj.value
            if fn is None:
                assert False, f"invalid operation 'invoke' called on property {method}"
            return fn(obj, args)
        elif hasattr(obj, method):
            fn = getattr(obj, method, None)
            return fn(obj, args)
        elif hasattr(obj, 'value'):
            val = obj.value
            if hasattr(val, method):
                fn = getattr(val, method, None)
                return fn(obj, args)
        assert False, f"method {method} undefined"


def ty2descriptor(v):
    if _NOT_INITED:
        init_type_proxies()
    ty = type(v).__name__.lower()
    if ty in _type_aliases:
        ty = _type_aliases[ty]
    if ty not in _descriptors:
        return None
    return _descriptors[ty]


def init_type_proxies():
    global _NOT_INITED
    _NOT_INITED = False
    for _type_name, _members in _descriptors.items():
        o = Descriptor(ty=_type_name, members=_members)
        _descriptors[_type_name] = o


_descriptors = {
    #              prop   INVOKE  GET  PUT   GETIDX   PUTIDX
    'dataframe': {'_': (None, None, None, None, df_set_at),
                  'axes': (df_axes, None, None, None, None),
                  'clip': (df_clip, None, None, None, None),
                  'columns': (df_columns, df_columns, df_set_columns, None, df_set_idx_columns),
                  'empty': (df_empty, None, None, None, None),
                  'flags': (df_set_flags, None, None, None, None),
                  'head': (df_head, None, None, None, None),
                  'index': (df_index, None, None, None, None),
                  'info': (df_info, None, None, None, None),
                  'shape': (df_shape, None, None, None, None),
                  'trim': (pd_trim, None,  None, None, None),
                  'values': (df_values, None, None, None, None),
                  },
}

_type_aliases = {
    'dataset': 'dataframe',
}