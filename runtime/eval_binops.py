from runtime.conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from runtime.environment import Environment
from runtime.exceptions import runtime_error
from runtime.token_ids import TK


from runtime.eval_boolean import _boolean_dispatch_table, eval_boolean_dispatch


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_BINOPS_TOKENS = [
    TK.ADD, 
    TK.SUB, 
    TK.DIV, 
    TK.IDIV, 
    TK.POW, 
    TK.MUL, 
    TK.MOD, 
]

_INTRINSIC_VALUE_TYPES = ['any', 'int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block', 'DataFrame', 'Range', 'Series', 'Set', 'list']

_type2idx = {
    'any': 0,
    'int': 1,
    'float': 2,
    'bool': 3,
    'str': 4,
    'timedelta': 5,
    'Object': 6,
    'Block': 7,
    'DataFrame': 8,
    'Range': 9,
    'Series': 10,
    'Set': 11,
    'list': 12,
}

_type2native = {
    'Bool': 'bool',
    'DataFrame': 'dateframe',
    'DateTime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'Ident': 'ident',
    'Int': 'int',
    'List': 'list',
    'Percent': 'float',
    'Range': 'range',
    'Series': 'series',
    'Str': 'str',
    'Time': 'datetime',
}


# --------------------------------------------------
#            M A N U A L   C H A N G E S 
# --------------------------------------------------
def is_supported_binop(op):
    return op in _binops_dispatch_table or op in _boolean_dispatch_table


# used by fixups
def eval_binops_dispatch_fixup(node):
    if node is None:
        return None
    if node.op in _binops_dispatch_table:
        return eval_binops_dispatch(node, node.left, node.right)
    if node.op in _boolean_dispatch_table:
        return eval_boolean_dispatch(node, node.left, node.right)
    return node.value


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_binops_dispatch(node, left, right):
    l_value = left
    l_ty = type(l_value).__name__
    if hasattr(left, 'value') or l_ty in ['Int', 'Bool', 'Str', 'Float']:
        l_value = left.value
        l_ty = type(l_value).__name__
    r_value = right
    r_ty = type(r_value).__name__
    if hasattr(right, 'value') or r_ty in ['Int', 'Bool', 'Str', 'Float']:
        r_value = right.value
        r_ty = type(r_value).__name__
    if l_ty == 'Ident':
        l_value = Environment.current.scope.find(left.token).value
    if r_ty == 'Ident':
        r_value = Environment.current.scope.find(right.token).value
    if l_value is None or r_value is None:
        return None
    return eval_binops_dispatch2(node.op, l_value, r_value)


def eval_binops_dispatch2(tkid, l_value, r_value):
    l_ty = type(l_value).__name__
    r_ty = type(r_value).__name__
    l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]
    r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]
    if l_ty in _type2idx and r_ty in _type2idx:
        ixl = _type2idx[l_ty]
        ixr = _type2idx[r_ty]
        fn = _binops_dispatch_table[tkid][ixr][ixl]
        return fn(l_value, r_value)


# --------------------------------------------------
#        O P E R A T O R   F U N C T I O N S 
# --------------------------------------------------


def _add__any_any(l_value, r_value):
    return l_value + r_value


def _add__str_any(l_value, r_value):
    return l_value + f'{r_value}'


def _add__object_int(l_value, r_value):
    return c_unbox(l_value) + r_value


def _add__any_str(l_value, r_value):
    return f'{l_value}' + r_value


def _add__int_object(l_value, r_value):
    return l_value + c_unbox(r_value)


def _add__series_series(l_value, r_value):
    return sadd(l_value,r_value)


def _add__set_set(l_value, r_value):
    return s2add(1,r_value)


def _add__list_list(l_value, r_value):
    return ladd(1,r_value)


def _sub__any_any(l_value, r_value):
    return l_value - r_value


def _sub__object_int(l_value, r_value):
    return c_unbox(l_value) - r_value


def _sub__int_object(l_value, r_value):
    return l_value - c_unbox(r_value)


def _sub__series_series(l_value, r_value):
    return ssub(l_value,r_value)


def _sub__set_set(l_value, r_value):
    return s2sub(l_value,r_value)


def _sub__list_list(l_value, r_value):
    return lsub(l_value,r_value)


def _div__any_any(l_value, r_value):
    return l_value / r_value


def _div__object_int(l_value, r_value):
    return c_unbox(l_value) / r_value


def _div__int_object(l_value, r_value):
    return l_value / c_unbox(r_value)


def _div__series_series(l_value, r_value):
    return sdiv(l_value,r_value)


def _div__set_set(l_value, r_value):
    return s2div(l_value,r_value)


def _div__list_list(l_value, r_value):
    return ldiv(l_value,r_value)


def _idiv__any_any(l_value, r_value):
    return l_value // r_value


def _idiv__object_int(l_value, r_value):
    return c_unbox(l_value) // r_value


def _idiv__int_object(l_value, r_value):
    return l_value // c_unbox(r_value)


def _idiv__series_series(l_value, r_value):
    return sidiv(l_value,r_value)


def _idiv__set_set(l_value, r_value):
    return s2idiv(l_value,r_value)


def _idiv__list_list(l_value, r_value):
    return lidiv(l_value,r_value)


def _pow__any_any(l_value, r_value):
    return l_value ** r_value


def _pow__object_int(l_value, r_value):
    return c_unbox(l_value) ** r_value


def _pow__int_object(l_value, r_value):
    return l_value ** c_unbox(r_value)


def _mul__any_any(l_value, r_value):
    return l_value * r_value


def _mul__object_int(l_value, r_value):
    return c_unbox(l_value) * r_value


def _mul__int_object(l_value, r_value):
    return l_value * c_unbox(r_value)


def _mul__series_range(l_value, r_value):
    return lrmul(l_value,r_value)


def _mul__series_series(l_value, r_value):
    return smul(l_value,r_value)


def _mul__set_set(l_value, r_value):
    return s2mul(l_value,r_value)


def _mul__list_list(l_value, r_value):
    return lmul(l_value,r_value)


def _mod__any_any(l_value, r_value):
    return l_value % r_value


def _mod__object_int(l_value, r_value):
    return c_unbox(l_value) % r_value


def _mod__int_object(l_value, r_value):
    return l_value % c_unbox(r_value)


def _mod__series_series(l_value, r_value):
    return smod(l_value,r_value)


def _mod__set_set(l_value, r_value):
    return s2mod(l_value,r_value)


def _mod__list_list(l_value, r_value):
    return lmod(l_value,r_value)


# --------------------------------------------------
#           E R R O R   F U N C T I O N S 
# --------------------------------------------------


def _invalid_add(left, right):
    runtime_error(f'Type mismatch for operator add({type(left)}, {type(right)})', loc=None)


def _invalid_sub(left, right):
    runtime_error(f'Type mismatch for operator sub({type(left)}, {type(right)})', loc=None)


def _invalid_div(left, right):
    runtime_error(f'Type mismatch for operator div({type(left)}, {type(right)})', loc=None)


def _invalid_idiv(left, right):
    runtime_error(f'Type mismatch for operator idiv({type(left)}, {type(right)})', loc=None)


def _invalid_pow(left, right):
    runtime_error(f'Type mismatch for operator pow({type(left)}, {type(right)})', loc=None)


def _invalid_mul(left, right):
    runtime_error(f'Type mismatch for operator mul({type(left)}, {type(right)})', loc=None)


def _invalid_mod(left, right):
    runtime_error(f'Type mismatch for operator mod({type(left)}, {type(right)})', loc=None)


# --------------------------------------------------
#            D I S P A T C H   T A B L E 
# --------------------------------------------------
_binops_dispatch_table = {
    TK.ADD: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # any  
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__object_int, _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # int  
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # float  
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # bool  
        [_add__any_str,    _add__any_any,    _add__any_any,    _add__any_str,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # str  
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # timedelta  
        [_add__any_any,    _add__int_object, _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Object  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Block  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # DataFrame  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Range  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__series_series, _invalid_add,     _invalid_add],   # Series  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__set_set,    _invalid_add],   # Set  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__list_list],   # list  
    
        ],
    TK.SUB: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # any  
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__object_int, _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # int  
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # float  
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # bool  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # str  
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # timedelta  
        [_sub__any_any,    _sub__int_object, _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Object  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Block  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # DataFrame  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Range  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__series_series, _invalid_sub,     _invalid_sub],   # Series  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__set_set,    _invalid_sub],   # Set  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__list_list],   # list  
    
        ],
    TK.DIV: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # any  
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__object_int, _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # int  
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # float  
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # bool  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # str  
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # timedelta  
        [_div__any_any,    _div__int_object, _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Object  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Block  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # DataFrame  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Range  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__series_series, _invalid_div,     _invalid_div],   # Series  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__set_set,    _invalid_div],   # Set  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__list_list],   # list  
    
        ],
    TK.IDIV: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # any  
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__object_int, _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # int  
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # float  
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # bool  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # str  
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # timedelta  
        [_idiv__any_any,   _idiv__int_object, _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Object  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Block  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # DataFrame  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Range  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__series_series, _invalid_idiv,    _invalid_idiv],   # Series  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__set_set,   _invalid_idiv],   # Set  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__list_list],   # list  
    
        ],
    TK.POW: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # any  
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__object_int, _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # int  
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # float  
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # bool  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # str  
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # timedelta  
        [_pow__any_any,    _pow__int_object, _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Object  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Block  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # DataFrame  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Range  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Series  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Set  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # list  
    
        ],
    TK.MUL: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # any  
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__object_int, _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # int  
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # float  
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # bool  
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # str  
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # timedelta  
        [_mul__any_any,    _mul__int_object, _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # Object  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # Block  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # DataFrame  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__series_range, _invalid_mul,     _invalid_mul],   # Range  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__series_series, _invalid_mul,     _invalid_mul],   # Series  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__set_set,    _invalid_mul],   # Set  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__list_list],   # list  
    
        ],
    TK.MOD: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # any  
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__object_int, _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # int  
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # float  
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # bool  
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # str  
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # timedelta  
        [_mod__any_any,    _mod__int_object, _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Object  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Block  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # DataFrame  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Range  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__series_series, _invalid_mod,     _invalid_mod],   # Series  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__set_set,    _invalid_mod],   # Set  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__list_list],   # list  
    
        ],
}
