from tokens import TK

from environment import Environment
from exceptions import runtime_error

_SUPPORTED_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'object', 'block']
_SUPPORTED_ASSIGNMENT_TOKENS = [TK.APPLY, TK.ASSIGN, TK.DEFINE]

_type2idx = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'str': 3,
    'timedelta': 4,
    'object': 5,
    'block': 6,
}

_type2native = {
    'Ident': 'ident',
    'Block': 'block',
    'Bool': 'bool',
    'DateTime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'Int': 'int',
    'Object': 'object',
    'Percent': 'float',
    'Str': 'str',
    'Time': 'datetime',
}


def eval_assignment_dispatch(left, right):
    l_value = left
    if getattr(left, 'value', False):
        l_value = left.value
    l_ty = type(l_value).__name__
    r_value = right
    if getattr(right, 'value', False):
        r_value = right.value
    r_ty = type(r_value).__name__
    if l_ty == 'Ident':
        l_value = Environment.current.scope.find(left.token).value
    if r_ty == 'Ident':
        r_value = Environment.current.scope.find(right.token).value
    if l_value is None or r_value is None:
        return None
    return eval_assignment_dispatch2(l_value, r_value)


def eval_assignment_dispatch2(l_value, r_value):
    l_ty = type(l_value).__name__
    r_ty = type(r_value).__name__
    l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]
    r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]
    if l_ty in _type2idx and r_ty in _type2idx:
        ixl = _type2idx[l_ty]
        ixr = _type2idx[r_ty]
        fn = _assignment_dispatch_table[ixl][ixr]
        return fn(l_value, r_value)


def _assign__int_int(l_value, r_value):
    l_value = r_value
    return l_value


def _assign__any_object(l_value, r_value):
    l_value.value = r_value
    return l_value


def _assign__block_object(l_value, r_value):
    l_value.from_block(r_value)
    return l_value


def _assign__object_block(l_value, r_value):
    l_value = r_value
    runtime_error(f'Not Implemented: _assign__object_block', loc=None)
    return l_value


def _assign__object_object(l_value, r_value):
    l_value = r_value
    runtime_error(f'Not Implemented: _assign__object_object', loc=None)
    return l_value


def _invalid_assign(left, right):
    runtime_error(f'Type mismatch for assignment({type(left)}, {type(right)})', loc=None)


_assignment_dispatch_table = [  # l-values (column:from) x r-values (rows:to)
    #      int                 float                  bool                 str                timedelta           Object                  Block
    [_assign__int_int,    _assign__int_int,     _assign__int_int,   _assign__int_int,     _assign__int_int,   _invalid_assign,       _invalid_assign],   # int
    [_assign__int_int,    _assign__int_int,     _assign__int_int,   _assign__int_int,     _assign__int_int,   _invalid_assign,       _invalid_assign],   # float
    [_assign__int_int,    _assign__int_int,     _assign__int_int,   _assign__int_int,     _assign__int_int,   _invalid_assign,       _invalid_assign],   # bool
    [_assign__int_int,    _assign__int_int,     _invalid_assign,    _assign__int_int,     _invalid_assign,    _invalid_assign,       _invalid_assign],   # str
    [_assign__int_int,    _assign__int_int,     _assign__int_int,   _assign__int_int,     _assign__int_int,   _invalid_assign,       _invalid_assign],   # timedelta
    [_assign__any_object, _assign__any_object,  _assign__any_object, _assign__any_object, _assign__any_object,_assign__object_object, _assign__block_object],   # Object
    [_invalid_assign,     _invalid_assign,      _invalid_assign,    _invalid_assign,      _invalid_assign,    _assign__object_block, _assign__int_int],   # Block
]


