#!/Users/jim/venv/jimc/bin/python

"""
IndexedDict:

A class similar to namedtuple in that members can be accessed either by index, or by named property.  Additionally,
they can be accessed by named key similar to a dictionary, but also the keys may be accessed by index similar to a
list.  This list is in insertion order per the underlying dict() class.  Unlike namedtuple(), the set of keys may
be expanded upon after creation.

The focus of this class is for implementing parameter list structures where there
may be a combination of named parameters as well as sequentially ordered parameters.  In this case, the keys for
un-named parameters are created during addition, yet the recipient is free to access the parameters by index.

This is also used to implement the Options class, where the focus is on accessing the members by key or by property.
In both cases, the ability to update the keys after construction is a critical feature.

"""
from copy import deepcopy


class IndexedDict(object):

    def __init__(self, items=None, defaults=None):
        super().__init__()
        self._defaults = {} if defaults is None else defaults
        if defaults is not None:
            self.__dict__.update(self._defaults)
        if items is not None:
            self.__dict__.update(items)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get_item_by_index(key)
        return self._get_item_by_key(key, self._get_default(key, None))

    def __setitem__(self, key, value):
        self._set_item_by_key(key, value)

    def items(self):
        k = list(self.__dict__.items())
        return k[1:]

    def keys(self, keys=None):
        k = list(self.__dict__.keys())[1:]
        return k

    def values(self):
        k = list(self.__dict__.values())
        return k[1:]

    def to_dict(self, keys=None):
        d = deepcopy(self._defaults)
        d.update(self.__dict__)
        if keys is not None:
            k = {}
            for ky in keys:
                if ky in d:
                    k[ky] = d[ky]
            d = k
        return d

    def update(self, items):
        self.__dict__.update(items)

    def _get_item_by_index(self, index, default=None):
        keys = list(self.__dict__.keys())
        index += 1  # _defaults takes the first slot
        if index < 0 or index > len(keys):
            raise IndexError('Index out of range')
        return self._get_item_by_key(keys[index], default)

    def _set_item_by_index(self, index, value=None):
        keys = list(self.__dict__.keys())
        if index < 0 or index > len(keys):
            raise IndexError('Index out of range')
        return self._set_item_by_key(keys[index], value)

    def _get_item_by_key(self, key, default=None):
        if key not in self.__dict__:
            return default
        return self.__dict__[key]

    def _set_item_by_key(self, key, value=None):
        self.__dict__[key] = value

    def _get_default(self, key, default):
        return default if key not in self._defaults else self._defaults[key]


if __name__ == '__main__':
    d = IndexedDict(items={'strict':False}, defaults={'strict':False, 'force':False})
    print(d.strict)
    print(d[0])
    print(d['force'])
    d['force'] = True
    print(d['force'])
    print(d[1])
    print(d.force)
    print(d.keys())
    print(d.values())
    print(d.items())
