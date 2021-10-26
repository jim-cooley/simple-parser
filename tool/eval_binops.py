from exceptions import _runtime_error, _error
from tokens import TK

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'str']


_type2idx = {
    'int': 1,
    'float': 2,
    'bool': 3,
    'str': 4,
}


_binops_dispatch_table = {

    TK.ADD: [
        #      int           float           bool           str           
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int],   # int      
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int],   # float      
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int],   # bool      
        [_add__int_str, _add__int_str, _add__int_str, _add__int_int],   # str      
    
    ],
    TK.SUB: [
        #      int           float           bool           str           
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub],   # int      
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub],   # float      
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub],   # bool      
        [_invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub],   # str      
    
    ],
    TK.DIV: [
        #      int           float           bool           str           
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div],   # int      
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div],   # float      
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div],   # bool      
        [_invalid_div, _invalid_div, _invalid_div, _invalid_div],   # str      
    
    ],
    TK.POW: [
        #      int           float           bool           str           
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow],   # int      
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow],   # float      
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow],   # bool      
        [_invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow],   # str      
    
    ],
    TK.MUL: [
        #      int           float           bool           str           
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # int      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # float      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # bool      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # str      
    
    ],
}


def eval_binops_dispatch(node):
    if node.token.id in _binops_dispatch_table:
        left = node.left
        l_ty = type(left.value).__name__
        right = node.right
        r_ty = type(right.value).__name__
        if l_ty in _type2idx and r_ty in _type2idx:
            ixl = _type2idx[l_ty]
            ixr = _type2idx[r_ty]
            fn = _binops_dispatch_table[node.token.id][ixr][ixl]
            return fn(left, right)
    _error(f'Invalid operation {node.token.id.name}', loc=node.token.location)


def _add__int_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value + r_value


def _add__str_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value + f'{r_value}'


def _add__int_str(left, right):
    l_value = left.value
    r_value = right.value
    return f'{l_value}' + r_value


def _sub__int_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value - r_value


def _div__int_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value / r_value


def _pow__int_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value ** r_value


def _mul__int_int(left, right):
    l_value = left.value
    r_value = right.value
    return l_value * r_value


def _invalid_add(left, right):
    _runtime_error(f'Type mismatch for operator add({type(left)}, {type(right)})', loc=None)


def _invalid_sub(left, right):
    _runtime_error(f'Type mismatch for operator sub({type(left)}, {type(right)})', loc=None)


def _invalid_div(left, right):
    _runtime_error(f'Type mismatch for operator div({type(left)}, {type(right)})', loc=None)


def _invalid_pow(left, right):
    _runtime_error(f'Type mismatch for operator pow({type(left)}, {type(right)})', loc=None)


def _invalid_mul(left, right):
    _runtime_error(f'Type mismatch for operator mul({type(left)}, {type(right)})', loc=None)


