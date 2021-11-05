from conversion import c_box, c_to_bool, c_to_int, c_unbox
from environment import Environment
from exceptions import runtime_error
from scope import Object
from tokens import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_INTRINSIC_VALUE_TYPES = ['any', 'int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block']

_type2idx = {
    'any': 0,
    'int': 1,
    'float': 2,
    'bool': 3,
    'str': 4,
    'timedelta': 5,
    'Object': 6,
    'Block': 7,
}

_type2native = {
    'Ident': 'ident',
    'Bool': 'bool',
    'DateTime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'Int': 'int',
    'Percent': 'float',
    'Str': 'str',
    'Time': 'datetime',
}


# --------------------------------------------------
#            M A N U A L   C H A N G E S 
# --------------------------------------------------
# used by fixups
def eval_binops_dispatch_fixup(node):
    if node is None:
        return None
    if node.op in _binops_dispatch_table:
        return eval_binops_dispatch(node, node.left, node.right)
    return node.value


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_binops_dispatch(node, left, right):
    l_value = c_unbox(left)
    l_ty = type(l_value).__name__
    r_value = c_unbox(right)
    r_ty = type(r_value).__name__
    if l_ty == 'Ident':
        l_value = Environment.current.scope.find(left.token).value
    if r_ty == 'Ident':
        r_value = Environment.current.scope.find(right.token).value
    if l_value is None or r_value is None:
        return None
    return eval_binops_dispatch2(node.token.id, l_value, r_value)


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


def _add__int_str(l_value, r_value):
    return f'{l_value}' + r_value


def _add__int_object(l_value, r_value):
    return l_value + c_unbox(r_value)


def _sub__any_any(l_value, r_value):
    return l_value - r_value


def _sub__object_int(l_value, r_value):
    return c_unbox(l_value) - r_value


def _sub__int_object(l_value, r_value):
    return l_value - c_unbox(r_value)


def _div__any_any(l_value, r_value):
    return l_value / r_value


def _div__object_int(l_value, r_value):
    return c_unbox(l_value) / r_value


def _div__int_object(l_value, r_value):
    return l_value / c_unbox(r_value)


def _idiv__any_any(l_value, r_value):
    return l_value // r_value


def _idiv__object_int(l_value, r_value):
    return c_unbox(l_value) // r_value


def _idiv__int_object(l_value, r_value):
    return l_value // c_unbox(r_value)


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


def _mod__any_any(l_value, r_value):
    return l_value % r_value


def _mod__object_int(l_value, r_value):
    return c_unbox(l_value) % r_value


def _mod__int_object(l_value, r_value):
    return l_value % c_unbox(r_value)


def _and__any_any(l_value, r_value):
    return l_value and r_value


def _iseq__any_any(l_value, r_value):
    return l_value == r_value


def _iseq__bool_int(l_value, r_value):
    return l_value == c_to_bool(r_value, TK.INT)


def _iseq__int_bool(l_value, r_value):
    return l_value == c_to_int(r_value, TK.BOOL)


def _neq__any_any(l_value, r_value):
    return l_value != r_value


def _neq__bool_int(l_value, r_value):
    return l_value != c_to_bool(r_value, TK.INT)


def _neq__int_bool(l_value, r_value):
    return l_value != c_to_int(r_value, TK.BOOL)


def _gtr__any_any(l_value, r_value):
    return l_value > r_value


def _less__any_any(l_value, r_value):
    return l_value < r_value


def _gte__any_any(l_value, r_value):
    return l_value >= r_value


def _lte__any_any(l_value, r_value):
    return l_value <= r_value


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


def _invalid_and(left, right):
    runtime_error(f'Type mismatch for operator and({type(left)}, {type(right)})', loc=None)


def _invalid_or(left, right):
    runtime_error(f'Type mismatch for operator or({type(left)}, {type(right)})', loc=None)


def _invalid_iseq(left, right):
    runtime_error(f'Type mismatch for operator iseq({type(left)}, {type(right)})', loc=None)


def _invalid_neq(left, right):
    runtime_error(f'Type mismatch for operator neq({type(left)}, {type(right)})', loc=None)


def _invalid_gtr(left, right):
    runtime_error(f'Type mismatch for operator gtr({type(left)}, {type(right)})', loc=None)


def _invalid_less(left, right):
    runtime_error(f'Type mismatch for operator less({type(left)}, {type(right)})', loc=None)


def _invalid_gte(left, right):
    runtime_error(f'Type mismatch for operator gte({type(left)}, {type(right)})', loc=None)


def _invalid_lte(left, right):
    runtime_error(f'Type mismatch for operator lte({type(left)}, {type(right)})', loc=None)


# --------------------------------------------------
#            D I S P A T C H   T A B L E 
# --------------------------------------------------
_binops_dispatch_table = {
    TK.ADD: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_add__any_any, _add__any_any, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__any_any, _invalid_add],   # any      
        [_add__any_any, _add__any_any, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__object_int, _invalid_add],   # int      
        [_add__any_any, _add__any_any, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__any_any, _invalid_add],   # float      
        [_add__any_any, _add__any_any, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__any_any, _invalid_add],   # bool      
        [_add__any_str, _add__int_str, _add__int_str, _add__int_str, _invalid_add, _invalid_add, _invalid_add, _invalid_add],   # str      
        [_add__any_any, _add__any_any, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__any_any, _invalid_add],   # timedelta      
        [_add__any_any, _add__int_object, _add__any_any, _add__any_any, _add__str_any, _add__any_any, _add__any_any, _invalid_add],   # Object      
        [_invalid_add, _invalid_add, _invalid_add, _invalid_add, _invalid_add, _invalid_add, _invalid_add, _invalid_add],   # Block      
    
    ],
    TK.SUB: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_sub__any_any, _sub__any_any, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # any      
        [_sub__any_any, _sub__any_any, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__object_int, _invalid_sub],   # int      
        [_sub__any_any, _sub__any_any, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # float      
        [_sub__any_any, _sub__any_any, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # bool      
        [_invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # str      
        [_sub__any_any, _sub__any_any, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # timedelta      
        [_sub__any_any, _sub__int_object, _sub__any_any, _sub__any_any, _invalid_sub, _sub__any_any, _sub__any_any, _invalid_sub],   # Object      
        [_invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub, _invalid_sub],   # Block      
    
    ],
    TK.DIV: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_div__any_any, _div__any_any, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # any      
        [_div__any_any, _div__any_any, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__object_int, _invalid_div],   # int      
        [_div__any_any, _div__any_any, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # float      
        [_div__any_any, _div__any_any, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # bool      
        [_invalid_div, _invalid_div, _invalid_div, _invalid_div, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # str      
        [_div__any_any, _div__any_any, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # timedelta      
        [_div__any_any, _div__int_object, _div__any_any, _div__any_any, _invalid_div, _div__any_any, _div__any_any, _invalid_div],   # Object      
        [_invalid_div, _invalid_div, _invalid_div, _invalid_div, _invalid_div, _invalid_div, _invalid_div, _invalid_div],   # Block      
    
    ],
    TK.IDIV: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_idiv__any_any, _idiv__any_any, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # any      
        [_idiv__any_any, _idiv__any_any, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__object_int, _invalid_idiv],   # int      
        [_idiv__any_any, _idiv__any_any, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # float      
        [_idiv__any_any, _idiv__any_any, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # bool      
        [_invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # str      
        [_idiv__any_any, _idiv__any_any, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # timedelta      
        [_idiv__any_any, _idiv__int_object, _idiv__any_any, _idiv__any_any, _invalid_idiv, _idiv__any_any, _idiv__any_any, _invalid_idiv],   # Object      
        [_invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv, _invalid_idiv],   # Block      
    
    ],
    TK.POW: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_pow__any_any, _pow__any_any, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # any      
        [_pow__any_any, _pow__any_any, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__object_int, _invalid_pow],   # int      
        [_pow__any_any, _pow__any_any, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # float      
        [_pow__any_any, _pow__any_any, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # bool      
        [_invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # str      
        [_pow__any_any, _pow__any_any, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # timedelta      
        [_pow__any_any, _pow__int_object, _pow__any_any, _pow__any_any, _invalid_pow, _pow__any_any, _pow__any_any, _invalid_pow],   # Object      
        [_invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow, _invalid_pow],   # Block      
    
    ],
    TK.MUL: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _invalid_mul],   # any      
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__object_int, _invalid_mul],   # int      
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _invalid_mul],   # float      
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _invalid_mul, _mul__any_any, _mul__any_any, _invalid_mul],   # bool      
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _invalid_mul, _mul__any_any, _mul__any_any, _invalid_mul],   # str      
        [_mul__any_any, _mul__any_any, _mul__any_any, _mul__any_any, _invalid_mul, _mul__any_any, _mul__any_any, _invalid_mul],   # timedelta      
        [_mul__any_any, _mul__int_object, _mul__any_any, _mul__any_any, _invalid_mul, _mul__any_any, _mul__any_any, _invalid_mul],   # Object      
        [_invalid_mul, _invalid_mul, _invalid_mul, _invalid_mul, _invalid_mul, _invalid_mul, _invalid_mul, _invalid_mul],   # Block      
    
    ],
    TK.MOD: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # any      
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__object_int, _invalid_mod],   # int      
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # float      
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # bool      
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # str      
        [_mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # timedelta      
        [_mod__any_any, _mod__int_object, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _mod__any_any, _invalid_mod],   # Object      
        [_invalid_mod, _invalid_mod, _invalid_mod, _invalid_mod, _invalid_mod, _invalid_mod, _invalid_mod, _invalid_mod],   # Block      
    
    ],
    TK.AND: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # any      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # int      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # float      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # bool      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # str      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_and],   # timedelta      
        [_invalid_and, _invalid_and, _invalid_and, _invalid_and, _invalid_and, _invalid_and, _invalid_and, _invalid_and],   # Object      
    
    ],
    TK.OR: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # any      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # int      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # float      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # bool      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # str      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # timedelta      
        [_and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _and__any_any, _invalid_or],   # Object      
        [_invalid_or, _invalid_or, _invalid_or, _invalid_or, _invalid_or, _invalid_or, _invalid_or, _invalid_or],   # Block      
    
    ],
    TK.ISEQ: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # any      
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__bool_int, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # int      
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # float      
        [_iseq__any_any, _iseq__int_bool, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # bool      
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # str      
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # timedelta      
        [_iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _iseq__any_any, _invalid_iseq],   # Object      
        [_invalid_iseq, _invalid_iseq, _invalid_iseq, _invalid_iseq, _invalid_iseq, _invalid_iseq, _invalid_iseq, _invalid_iseq],   # Block      
    
    ],
    TK.NEQ: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # any      
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__bool_int, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # int      
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # float      
        [_neq__any_any, _neq__int_bool, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # bool      
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # str      
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # timedelta      
        [_neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _neq__any_any, _invalid_neq],   # Object      
        [_invalid_neq, _invalid_neq, _invalid_neq, _invalid_neq, _invalid_neq, _invalid_neq, _invalid_neq, _invalid_neq],   # Block      
    
    ],
    TK.GTR: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # any      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # int      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # float      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # bool      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # str      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # timedelta      
        [_gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _gtr__any_any, _invalid_gtr],   # Object      
        [_invalid_gtr, _invalid_gtr, _invalid_gtr, _invalid_gtr, _invalid_gtr, _invalid_gtr, _invalid_gtr, _invalid_gtr],   # Block      
    
    ],
    TK.LESS: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # any      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # int      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # float      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # bool      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # str      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # timedelta      
        [_less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _less__any_any, _invalid_less],   # Object      
        [_invalid_less, _invalid_less, _invalid_less, _invalid_less, _invalid_less, _invalid_less, _invalid_less, _invalid_less],   # Block      
    
    ],
    TK.GTE: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # any      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # int      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # float      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # bool      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # str      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # timedelta      
        [_gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _gte__any_any, _invalid_gte],   # Object      
        [_invalid_gte, _invalid_gte, _invalid_gte, _invalid_gte, _invalid_gte, _invalid_gte, _invalid_gte, _invalid_gte],   # Block      
    
    ],
    TK.LTE: [
        #      any       int       float       bool       str       timedelta       Object       Block       
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # any      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # int      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # float      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # bool      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # str      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # timedelta      
        [_lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _lte__any_any, _invalid_lte],   # Object      
        [_invalid_lte, _invalid_lte, _invalid_lte, _invalid_lte, _invalid_lte, _invalid_lte, _invalid_lte, _invalid_lte],   # Block      
    
    ],
}
