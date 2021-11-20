from conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from environment import Environment
from exceptions import runtime_error
from tokens import TK


from eval_boolean import _boolean_dispatch_table, eval_boolean_dispatch


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_BINOPS_OPERATIONS = [
    TK.ADD, 
    TK.SUB, 
    TK.DIV, 
    TK.IDIV, 
    TK.POW, 
    TK.MUL, 
    TK.MOD, 
]

_INTRINSIC_VALUE_TYPES = ['any', 'int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block', 'DataFrame', 'Range', 'Series']

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
}

_type2native = {
    'Bool': 'bool',
    'DataFrame': 'dateframe',
    'DateTime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'Ident': 'ident',
    'Int': 'int',
    'Percent': 'float',
    'Range': 'range',
    'Series': 'series',
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
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add],   # any      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__object_int, _invalid_add],   # int      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add],   # float      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add],   # bool      
        [_add__any_str,    _add__any_any,    _add__any_any,    _add__any_str,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # str      
        [_add__any_any,    _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add],   # timedelta      
        [_add__any_any,    _add__int_object, _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _invalid_add],   # Object      
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Block      
    
    ],
    TK.SUB: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # any      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__object_int, _invalid_sub],   # int      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # float      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # bool      
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # str      
        [_sub__any_any,    _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # timedelta      
        [_sub__any_any,    _sub__int_object, _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _invalid_sub],   # Object      
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Block      
    
    ],
    TK.DIV: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # any      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__object_int, _invalid_div],   # int      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # float      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # bool      
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # str      
        [_div__any_any,    _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # timedelta      
        [_div__any_any,    _div__int_object, _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _invalid_div],   # Object      
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Block      
    
    ],
    TK.IDIV: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # any      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__object_int, _invalid_idiv],   # int      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # float      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # bool      
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # str      
        [_idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # timedelta      
        [_idiv__any_any,   _idiv__int_object, _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _invalid_idiv],   # Object      
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Block      
    
    ],
    TK.POW: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # any      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__object_int, _invalid_pow],   # int      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # float      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # bool      
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # str      
        [_pow__any_any,    _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # timedelta      
        [_pow__any_any,    _pow__int_object, _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _invalid_pow],   # Object      
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Block      
    
    ],
    TK.MUL: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul],   # any      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__object_int, _invalid_mul],   # int      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul],   # float      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul],   # bool      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul],   # str      
        [_mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul],   # timedelta      
        [_mul__any_any,    _mul__int_object, _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _invalid_mul],   # Object      
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # Block      
    
    ],
    TK.MOD: [
        #       any               int              float              bool              str            timedelta           Object            Block           DataFrame           Range             Series      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # any      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__object_int, _invalid_mod],   # int      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # float      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # bool      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # str      
        [_mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # timedelta      
        [_mod__any_any,    _mod__int_object, _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod],   # Object      
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Block      
    
    ],
}
