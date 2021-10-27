from exceptions import _runtime_error, _error
from tokens import TK

_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta']


_type2idx = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'str': 3,
    'timedelta': 4,
}


def eval_binops_dispatch(node):
    if node.op in _binops_dispatch_table:
        l_value = node.left.value
        l_ty = type(l_value).__name__
        r_value = node.right.value
        r_ty = type(r_value).__name__
        if l_value is None or r_value is None:
            return None
        if l_ty in _type2idx and r_ty in _type2idx:
            ixl = _type2idx[l_ty]
            ixr = _type2idx[r_ty]
            fn = _binops_dispatch_table[node.token.id][ixr][ixl]
            return fn(l_value, r_value)
    _error(f'Invalid operation {node.token.id.name}', loc=node.token.location)


def _add__int_int(l_value, r_value):
    return l_value + r_value


def _add__str_int(l_value, r_value):
    return l_value + f'{r_value}'


def _add__int_str(l_value, r_value):
    return f'{l_value}' + r_value


def _sub__int_int(l_value, r_value):
    return l_value - r_value


def _div__int_int(l_value, r_value):
    return l_value / r_value


def _idiv__int_int(l_value, r_value):
    return l_value // r_value


def _pow__int_int(l_value, r_value):
    return l_value ** r_value


def _mul__int_int(l_value, r_value):
    return l_value * r_value


def _mod__int_int(l_value, r_value):
    return l_value % r_value


def _invalid_add(left, right):
    _runtime_error(f'Type mismatch for operator add({type(left)}, {type(right)})', loc=None)


def _invalid_sub(left, right):
    _runtime_error(f'Type mismatch for operator sub({type(left)}, {type(right)})', loc=None)


def _invalid_div(left, right):
    _runtime_error(f'Type mismatch for operator div({type(left)}, {type(right)})', loc=None)


def _invalid_idiv(left, right):
    _runtime_error(f'Type mismatch for operator idiv({type(left)}, {type(right)})', loc=None)


def _invalid_pow(left, right):
    _runtime_error(f'Type mismatch for operator pow({type(left)}, {type(right)})', loc=None)


def _invalid_mul(left, right):
    _runtime_error(f'Type mismatch for operator mul({type(left)}, {type(right)})', loc=None)


def _invalid_mod(left, right):
    _runtime_error(f'Type mismatch for operator mod({type(left)}, {type(right)})', loc=None)


_binops_dispatch_table = {

    TK.ADD: [
        #      int           float           bool           str           timedelta           
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int, _add__int_int],   # int      
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int, _add__int_int],   # float      
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int, _add__int_int],   # bool      
        [_add__int_str, _add__int_str, _add__int_str, _invalid_add, _invalid_add],   # str      
        [_add__int_int, _add__int_int, _add__int_int, _add__str_int, _add__int_int],   # timedelta      
    
    ],
    TK.SUB: [
        #      int           float           bool           str           timedelta           
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub, _sub__int_int],   # int      
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub, _sub__int_int],   # float      
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub, _sub__int_int],   # bool      
        [_invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _sub__int_int],   # str      
        [_sub__int_int, _sub__int_int, _sub__int_int, _invalid_sub, _sub__int_int],   # timedelta      
    
    ],
    TK.DIV: [
        #      int           float           bool           str           timedelta           
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div, _div__int_int],   # int      
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div, _div__int_int],   # float      
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div, _div__int_int],   # bool      
        [_invalid_div, _invalid_div, _invalid_div, _invalid_div, _div__int_int],   # str      
        [_div__int_int, _div__int_int, _div__int_int, _invalid_div, _div__int_int],   # timedelta      
    
    ],
    TK.IDIV: [
        #      int           float           bool           str           timedelta           
        [_idiv__int_int, _idiv__int_int, _idiv__int_int, _invalid_idiv, _idiv__int_int],   # int      
        [_idiv__int_int, _idiv__int_int, _idiv__int_int, _invalid_idiv, _idiv__int_int],   # float      
        [_idiv__int_int, _idiv__int_int, _idiv__int_int, _invalid_idiv, _idiv__int_int],   # bool      
        [_invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _idiv__int_int],   # str      
        [_idiv__int_int, _idiv__int_int, _idiv__int_int, _invalid_idiv, _idiv__int_int],   # timedelta      
    
    ],
    TK.POW: [
        #      int           float           bool           str           timedelta           
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow, _pow__int_int],   # int      
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow, _pow__int_int],   # float      
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow, _pow__int_int],   # bool      
        [_invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _pow__int_int],   # str      
        [_pow__int_int, _pow__int_int, _pow__int_int, _invalid_pow, _pow__int_int],   # timedelta      
    
    ],
    TK.MUL: [
        #      int           float           bool           str           timedelta           
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # int      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # float      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # bool      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # str      
        [_mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int, _mul__int_int],   # timedelta      
    
    ],
    TK.MOD: [
        #      int           float           bool           str           timedelta           
        [_mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int],   # int      
        [_mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int],   # float      
        [_mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int],   # bool      
        [_mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int],   # str      
        [_mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int, _mod__int_int],   # timedelta      
    
    ],
}

