from exceptions import _runtime_error, _error
from tokens import TK

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block']


_type2idx = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'str': 3,
    'timedelta': 4,
    'Object': 5,
    'Block': 6,
}


def eval_assign_dispatch(node):
    if node.op in _assign_dispatch_table:
        l_value = node.left.value
        l_ty = type(l_value).__name__
        r_value = node.right.value
        r_ty = type(r_value).__name__
        if l_value is None or r_value is None:
            return None
        if l_ty in _type2idx and r_ty in _type2idx:
            ixl = _type2idx[l_ty]
            ixr = _type2idx[r_ty]
            fn = _assign_dispatch_table[node.token.id][ixr][ixl]
            return fn(l_value, r_value)
    _error(f'Invalid operation {node.token.id.name}', loc=node.token.location)


def _assign__int_int(l_value, r_value):
    return l_value = r_value


def _assign__block_object(l_value, r_value):
    return l_value = o


def _assign__object_block(l_value, r_value):
    return l_value = b


def _invalid_assign(left, right):
    _runtime_error(f'Type mismatch for operator assign({type(left)}, {type(right)})', loc=None)


_assign_dispatch_table = {

    TK.ASSIGN: [
        #      int           float           bool           str           timedelta           Object           Block           
        [_assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _invalid_assign, _invalid_assign],   # int      
        [_assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _invalid_assign, _invalid_assign],   # float      
        [_assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _invalid_assign, _invalid_assign],   # bool      
        [_assign__int_int, _assign__int_int, _invalid_assign, _assign__int_int, _invalid_assign, _invalid_assign, _invalid_assign],   # str      
        [_assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _assign__int_int, _invalid_assign, _invalid_assign],   # timedelta      
        [_invalid_assign, _invalid_assign, _invalid_assign, _invalid_assign, _invalid_assign, _assign__int_int, _assign__block_object],   # Object      
        [_invalid_assign, _invalid_assign, _invalid_assign, _invalid_assign, _invalid_assign, _assign__object_block, _assign__int_int],   # Block      
    
    ],
}


