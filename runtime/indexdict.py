#!/Users/jim/venv/jimc/bin/python

from copy import deepcopy


class IndexedDict(object):
    """
    IndexedDict:

    A class similar to NamedTuple in that members can be accessed either by index, or by named property.  Additionally,
    they can be accessed by named key similar to a dictionary, but also the keys may be accessed by index similar to a
    list.  This list is in insertion order per the underlying dict() class.  Unlike namedtuple(), the set of keys may
    be expanded upon after creation.

    The focus of this class is for implementing parameter list structures where there
    may be a combination of named parameters as well as sequentially ordered parameters.  In this case, the keys for
    un-named parameters are created during addition, yet the recipient is free to access the parameters by index.

    This is also used to implement the Options class, where the focus is on accessing the members by key or by property.
    In both cases, the ability to update the keys after construction is a critical feature.

    """

    def __init__(self, items=None, fields=None, values=None, defaults=None):
        super().__init__()
        self._fields = None
        self._values = None
        _items = defaults or {}
        if items is not None:
            _items.update(items)
            self._fields = list(_items.keys())
            self._values = list(_items.values())
            self.__dict__.update(_items)
        else:
            if not values:
                self._fields = list(_items.keys())
                self._values = list(_items.values())
                self.__dict__.update(_items)
            else:
                for k in _items:
                    if k not in fields:
                        fields.append(k)
                        values.append(_items[k])
                self._fields = fields
                self._values = values
                if fields:
                    self.__dict__.update(_rzip(fields, values))

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key > len(self._values):
                raise IndexError('Index out of range')
            return self._values[key]
        if key not in self._fields:
            raise KeyError(f'Key {key} not in dictionary')
        key = self._fields.index[key]
        return self._values[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key < 0 or key > len(self._values):
                raise IndexError('Index out of range')
            self._values[key] = value
            key = self._fields[key]
        else:
            idx = self._fields.index(key)
            if idx < 0:
                self._fields.append(key)
                self._values.append(value)
            else:
                self._values[idx] = value
        if key in self.__dict__:
            self.__dict__[key] = value

    def __str__(self):
        return self.format()

    def __len__(self):
        return len(self._values)

    def append(self, key=None, value=None):
        if key:
            if key in self._fields:
                raise KeyError(f'Key {key} already in dictionary')
            self._fields.append(key)
            self.__dict__[key] = value
        self._values.append(value)

    def is_empty(self):
        return len(self._values) == 0

    def items(self):                        # UNDONE: should be generator/iterator
        return _rzip(self._fields, self._values)

    def keys(self, keys=None):              # UNDONE: iterator?
        return self._fields

    def remove(self, key):
        if isinstance(key, list):
            for k in key:
                if k in self._fields:
                    idx = self._fields.index(k)
                    del self._fields[idx]
                    del self._values[idx]
                    self.__dict__.pop(k, None)
        else:
            if key in self._fields:
                idx = self._fields.index(key)
                del self._fields[idx]
                del self._values[idx]
                self.__dict__.pop(key, None)

    def values(self):                       # UNDONE: iterator?
        return self._values

    def dict(self, keys=None, filter=None):
        if filter is None:
            filter = ['_values']
        _d = dict(zip(self._fields, self._values))
        if keys is not None:
            _k = {}
            for ky in keys:
                if ky in _d:
                    _k[ky] = _d[ky]
            _d = _k
        if filter is not None:
            for ky in filter:
                if ky in _d:
                    _d.pop(ky, None)
        return _d

    def to_list(self):
        return self._values

    def update(self, items):
        self.__dict__.update(items)
        for k in items:
            idx = self._fields.index(k)
            if idx >= 0:
                self._values[idx] = items[k]
            else:
                self._fields.append(k)
                self._values.append(items[k])

    def format(self, brief=True):
        if not len(self._values):
            return '{}'
        else:
            if not brief:
                fstr = ''
                _lenv, _lenf = len(self._values), len(self._fields)
                for idx in range(0, _lenv):
                    if idx < _lenf:
                        fstr += f'{self._fields[idx]}: {self._values[idx]}'
                    else:
                        fstr += f'{self._values[idx]}'
                    fstr += ',' if idx < _lenv else ''
            else:
                fstr = f'count={len(self.__dict__.keys())-1}'
            return '{' + f'{fstr}' + '}'


# Helpers:
def _rzip(*iterables):
    # zip('ABCD', 'xy') --> Cx Dy
    sentinel = object()
    iterators = [reversed(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            elem = next(it, sentinel)
            if elem is sentinel:
                return
            result.append(elem)
        yield tuple(result)


# Test Harness
if __name__ == '__main__':
    d = IndexedDict(items={'strict': False}, defaults={'strict': False, 'force': False})
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
