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

_INTRINSIC_VALUE_TYPES = ['any', 'none', 'int', 'float', 'bool', 'str', 'datetime', 'timedelta', 'Object', 'Block', 'DataFrame', 'Range', 'Series', 'Set', 'list', 'ndarray']

_type2native = {
    'Block': 'block',
    'Bool': 'bool',
    'bool': 'bool',
    'DataFrame': 'dataframe',
    'DateTime': 'datetime',
    'datetime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'float': 'float',
    'Ident': 'object',
    'Int': 'int',
    'int': 'int',
    'List': 'list',
    'list': 'list',
    'ndarray': 'ndarray',
    'NoneType': 'none',
    'Object': 'object',
    'object': 'object',
    'Percent': 'float',
    'Range': 'range',
    'Series': 'series',
    'Set': 'set',
    'Str': 'str',
    'str': 'str',
    'Time': 'datetime',
    'timedelta': 'timedelta',
}

_type2idx = {
    'Block': 9,
    'Bool': 4,
    'bool': 4,
    'DataFrame': 10,
    'DateTime': 6,
    'datetime': 6,
    'Duration': 7,
    'Float': 3,
    'float': 3,
    'Ident': 8,
    'Int': 2,
    'int': 2,
    'List': 14,
    'list': 14,
    'ndarray': 15,
    'NoneType': 1,
    'Object': 8,
    'object': 8,
    'Percent': 3,
    'Range': 11,
    'Series': 12,
    'Set': 13,
    'Str': 5,
    'str': 5,
    'Time': 6,
    'timedelta': 7,
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
    if hasattr(left, 'value'):
        l_value = left.value
    l_ty = _type2native[type(l_value).__name__]
    r_value = right
    if hasattr(right, 'value'):
        r_value = right.value
    r_ty = _type2native[type(r_value).__name__]
    return eval_binops_dispatch2(node.op, l_value, r_value, l_ty, r_ty)


def eval_binops_dispatch2(tkid, l_value, r_value, l_ty=None, r_ty=None):
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


def _add__dataframe_int(l_value, r_value):
    return add_dfi


def _add__series_int(l_value, r_value):
    return add_si


def _add__list_int(l_value, r_value):
    return add_li


def _add__any_str(l_value, r_value):
    return f'{l_value}' + r_value


def _add__dataframe_timedelta(l_value, r_value):
    return add_dftd


def _add__series_timedelta(l_value, r_value):
    return add_tds


def _add__list_timedelta(l_value, r_value):
    return add_tdl


def _add__int_object(l_value, r_value):
    return l_value + c_unbox(r_value)


def _add__dataframe_dataframe(l_value, r_value):
    return add_dfdf


def _add__series_dataframe(l_value, r_value):
    return sadd(l_value,r_value)


def _add__list_dataframe(l_value, r_value):
    return add_ldf


def _add__range_range(l_value, r_value):
    return add_rr


def _add__dataframe_series(l_value, r_value):
    return add_dfs


def _add__series_series(l_value, r_value):
    return add_ss


def _add__list_series(l_value, r_value):
    return add_ls


def _add__set_set(l_value, r_value):
    return add_stst


def _add__dataframe_list(l_value, r_value):
    return add_sfl


def _add__series_list(l_value, r_value):
    return add_sl


def _add__list_list(l_value, r_value):
    return add_ll


def _add__dataframe_ndarray(l_value, r_value):
    return add_dfl


def _sub__any_any(l_value, r_value):
    return l_value - r_value


def _sub__object_int(l_value, r_value):
    return c_unbox(l_value) - r_value


def _sub__dataframe_int(l_value, r_value):
    return sub_dfi


def _sub__series_int(l_value, r_value):
    return sub_si


def _sub__list_int(l_value, r_value):
    return sub_li


def _sub__dataframe_timedelta(l_value, r_value):
    return sub_dftd


def _sub__series_timedelta(l_value, r_value):
    return sub_std


def _sub__int_object(l_value, r_value):
    return l_value - c_unbox(r_value)


def _sub__dataframe_dataframe(l_value, r_value):
    return sub_dfdf


def _sub__series_dataframe(l_value, r_value):
    return ssub(l_value,r_value)


def _sub__range_range(l_value, r_value):
    return sub_rr


def _sub__series_series(l_value, r_value):
    return sub_ss


def _sub__set_set(l_value, r_value):
    return sub_stst


def _sub__list_list(l_value, r_value):
    return sub_ll


def _div__any_any(l_value, r_value):
    return l_value / r_value


def _div__object_int(l_value, r_value):
    return c_unbox(l_value) / r_value


def _div__dataframe_int(l_value, r_value):
    return div_dfi


def _div__series_int(l_value, r_value):
    return div_si


def _div__list_int(l_value, r_value):
    return div_li


def _div__int_object(l_value, r_value):
    return l_value / c_unbox(r_value)


def _div__dataframe_dataframe(l_value, r_value):
    return div_dfdf


def _div__series_dataframe(l_value, r_value):
    return sdiv(l_value,r_value)


def _div__range_range(l_value, r_value):
    return div_rr


def _div__series_series(l_value, r_value):
    return div_ss


def _div__set_set(l_value, r_value):
    return div_stst


def _div__list_list(l_value, r_value):
    return div_ll


def _idiv__any_any(l_value, r_value):
    return l_value // r_value


def _idiv__object_int(l_value, r_value):
    return c_unbox(l_value) // r_value


def _idiv__dataframe_int(l_value, r_value):
    return idiv_dfi


def _idiv__series_int(l_value, r_value):
    return idiv_si


def _idiv__list_int(l_value, r_value):
    return idiv_li


def _idiv__int_object(l_value, r_value):
    return l_value // c_unbox(r_value)


def _idiv__dataframe_dataframe(l_value, r_value):
    return idiv_dfdf


def _idiv__series_dataframe(l_value, r_value):
    return sidiv(l_value,r_value)


def _idiv__range_range(l_value, r_value):
    return idiv_rr


def _idiv__series_series(l_value, r_value):
    return idiv_ss


def _idiv__list_list(l_value, r_value):
    return idiv_ll


def _pow__any_any(l_value, r_value):
    return l_value ** r_value


def _pow__object_int(l_value, r_value):
    return c_unbox(l_value) ** r_value


def _pow__dataframe_int(l_value, r_value):
    return pow_dfi


def _pow__series_int(l_value, r_value):
    return pow_si


def _pow__list_int(l_value, r_value):
    return pow_li


def _pow__series_float(l_value, r_value):
    return pow_so


def _pow__int_object(l_value, r_value):
    return l_value ** c_unbox(r_value)


def _pow__dataframe_dataframe(l_value, r_value):
    return pow_dfdf


def _pow__range_range(l_value, r_value):
    return pow_rr


def _pow__series_series(l_value, r_value):
    return pow_ss


def _pow__set_set(l_value, r_value):
    return pow_stst


def _pow__list_list(l_value, r_value):
    return pow_ll


def _mul__any_any(l_value, r_value):
    return l_value * r_value


def _mul__object_int(l_value, r_value):
    return c_unbox(l_value) * r_value


def _mul__dataframe_int(l_value, r_value):
    return mul_dfi


def _mul__series_int(l_value, r_value):
    return mul_si


def _mul__list_int(l_value, r_value):
    return mul_li


def _mul__int_object(l_value, r_value):
    return l_value * c_unbox(r_value)


def _mul__series_block(l_value, r_value):
    return lrmul(l_value,r_value)


def _mul__dataframe_dataframe(l_value, r_value):
    return mul_dfdf


def _mul__series_dataframe(l_value, r_value):
    return smul(l_value,r_value)


def _mul__range_range(l_value, r_value):
    return mul_rr


def _mul__int_series(l_value, r_value):
    return i:*l


def _mul__series_series(l_value, r_value):
    return mul_ss


def _mul__set_set(l_value, r_value):
    return mul_stst


def _mul__list_list(l_value, r_value):
    return mul_ll


def _mod__any_any(l_value, r_value):
    return l_value % r_value


def _mod__object_int(l_value, r_value):
    return c_unbox(l_value) % r_value


def _mod__dataframe_int(l_value, r_value):
    return mod_si


def _mod__list_int(l_value, r_value):
    return mod_li


def _mod__int_object(l_value, r_value):
    return l_value % c_unbox(r_value)


def _mod__object_object(l_value, r_value):
    return c_unbox(l_value) % c_unbox(r_value)


def _mod__dataframe_dataframe(l_value, r_value):
    return mod_dfdf


def _mod__series_dataframe(l_value, r_value):
    return smod(l_value,r_value)


def _mod__range_range(l_value, r_value):
    return mod_rr


def _mod__series_series(l_value, r_value):
    return mod_ss


def _mod__set_set(l_value, r_value):
    return mod_stst


def _mod__list_list(l_value, r_value):
    return mod_ll


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
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # any  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # none  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__object_int, _invalid_add,     _add__dataframe_int, _invalid_add,     _add__series_int, _invalid_add,     _add__list_int,   _add__list_int],   # int  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__object_int, _invalid_add,     _add__dataframe_int, _invalid_add,     _add__series_int, _invalid_add,     _add__list_int,   _add__list_int],   # float  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__object_int, _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # bool  
        [_add__any_str,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_str,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # str  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__object_int, _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # datetime  
        [_add__any_any,    _invalid_add,     _add__any_any,    _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__object_int, _invalid_add,     _add__dataframe_timedelta, _invalid_add,     _add__series_timedelta, _invalid_add,     _add__list_timedelta, _add__list_timedelta],   # timedelta  
        [_add__any_any,    _invalid_add,     _add__int_object, _add__any_any,    _add__any_any,    _add__str_any,    _add__any_any,    _add__any_any,    _add__any_any,    _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Object  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Block  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__dataframe_dataframe, _invalid_add,     _add__series_dataframe, _invalid_add,     _add__list_dataframe, _add__list_dataframe],   # DataFrame  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__range_range, _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add],   # Range  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__dataframe_series, _invalid_add,     _add__series_series, _invalid_add,     _add__list_series, _add__list_series],   # Series  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__set_set,    _invalid_add,     _invalid_add],   # Set  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__dataframe_list, _invalid_add,     _add__series_list, _invalid_add,     _add__list_list,  _add__list_list],   # list  
        [_invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _invalid_add,     _add__dataframe_ndarray, _invalid_add,     _add__series_list, _invalid_add,     _add__list_list,  _add__list_list],   # ndarray  
    
        ],
    TK.SUB: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # any  
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # none  
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__object_int, _invalid_sub,     _sub__dataframe_int, _invalid_sub,     _sub__series_int, _invalid_sub,     _sub__list_int,   _sub__list_int],   # int  
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__object_int, _invalid_sub,     _sub__dataframe_int, _invalid_sub,     _sub__series_int, _invalid_sub,     _sub__list_int,   _sub__list_int],   # float  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # bool  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # str  
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__object_int, _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # datetime  
        [_sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__object_int, _invalid_sub,     _sub__dataframe_timedelta, _invalid_sub,     _sub__series_timedelta, _invalid_sub,     _invalid_sub,     _invalid_sub],   # timedelta  
        [_sub__any_any,    _invalid_sub,     _sub__int_object, _sub__any_any,    _sub__any_any,    _invalid_sub,     _sub__any_any,    _sub__any_any,    _sub__any_any,    _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Object  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Block  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__dataframe_dataframe, _invalid_sub,     _sub__series_dataframe, _invalid_sub,     _invalid_sub,     _invalid_sub],   # DataFrame  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__range_range, _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub],   # Range  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__series_series, _invalid_sub,     _invalid_sub,     _invalid_sub],   # Series  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__set_set,    _invalid_sub,     _invalid_sub],   # Set  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__list_list,  _sub__list_list],   # list  
        [_invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _invalid_sub,     _sub__list_list,  _sub__list_list],   # ndarray  
    
        ],
    TK.DIV: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # any  
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # none  
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__object_int, _invalid_div,     _div__dataframe_int, _invalid_div,     _div__series_int, _invalid_div,     _div__list_int,   _div__list_int],   # int  
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__object_int, _invalid_div,     _div__dataframe_int, _invalid_div,     _div__series_int, _invalid_div,     _div__list_int,   _div__list_int],   # float  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # bool  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # str  
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # datetime  
        [_div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # timedelta  
        [_div__any_any,    _invalid_div,     _div__int_object, _div__any_any,    _div__any_any,    _invalid_div,     _div__any_any,    _div__any_any,    _div__any_any,    _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Object  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Block  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__dataframe_dataframe, _invalid_div,     _div__series_dataframe, _invalid_div,     _invalid_div,     _invalid_div],   # DataFrame  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__range_range, _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div],   # Range  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__series_series, _invalid_div,     _invalid_div,     _invalid_div],   # Series  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__set_set,    _invalid_div,     _invalid_div],   # Set  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__list_list,  _div__list_list],   # list  
        [_invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _invalid_div,     _div__list_list,  _div__list_list],   # ndarray  
    
        ],
    TK.IDIV: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # any  
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # none  
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__object_int, _invalid_idiv,    _idiv__dataframe_int, _invalid_idiv,    _idiv__series_int, _invalid_idiv,    _idiv__list_int,  _idiv__list_int],   # int  
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__object_int, _invalid_idiv,    _idiv__dataframe_int, _invalid_idiv,    _idiv__series_int, _invalid_idiv,    _idiv__list_int,  _idiv__list_int],   # float  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # bool  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # str  
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # datetime  
        [_idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # timedelta  
        [_idiv__any_any,   _invalid_idiv,    _idiv__int_object, _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _idiv__any_any,   _idiv__any_any,   _idiv__any_any,   _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Object  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Block  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__dataframe_dataframe, _invalid_idiv,    _idiv__series_dataframe, _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # DataFrame  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__range_range, _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Range  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__series_series, _invalid_idiv,    _invalid_idiv,    _invalid_idiv],   # Series  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__series_series, _invalid_idiv,    _invalid_idiv],   # Set  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__list_list, _idiv__list_list],   # list  
        [_invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _invalid_idiv,    _idiv__list_list, _idiv__list_list],   # ndarray  
    
        ],
    TK.POW: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # any  
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # none  
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__object_int, _invalid_pow,     _pow__dataframe_int, _invalid_pow,     _pow__series_int, _invalid_pow,     _pow__list_int,   _pow__list_int],   # int  
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__object_int, _invalid_pow,     _pow__dataframe_int, _invalid_pow,     _pow__series_float, _invalid_pow,     _pow__list_int,   _pow__list_int],   # float  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # bool  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # str  
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # datetime  
        [_pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # timedelta  
        [_pow__any_any,    _invalid_pow,     _pow__int_object, _pow__any_any,    _pow__any_any,    _invalid_pow,     _pow__any_any,    _pow__any_any,    _pow__any_any,    _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Object  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Block  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__dataframe_dataframe, _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # DataFrame  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__range_range, _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow],   # Range  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__series_series, _invalid_pow,     _invalid_pow,     _invalid_pow],   # Series  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__set_set,    _invalid_pow,     _invalid_pow],   # Set  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__list_list,  _pow__list_list],   # list  
        [_invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _invalid_pow,     _pow__list_list,  _pow__list_list],   # ndarray  
    
        ],
    TK.MUL: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # any  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # none  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__object_int, _invalid_mul,     _mul__dataframe_int, _invalid_mul,     _mul__series_int, _invalid_mul,     _mul__list_int,   _mul__list_int],   # int  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__any_any,    _mul__object_int, _invalid_mul,     _mul__dataframe_int, _invalid_mul,     _mul__series_int, _invalid_mul,     _mul__list_int,   _mul__list_int],   # float  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # bool  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # str  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # datetime  
        [_mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # timedelta  
        [_mul__any_any,    _invalid_mul,     _mul__int_object, _mul__any_any,    _mul__any_any,    _invalid_mul,     _mul__any_any,    _mul__any_any,    _mul__any_any,    _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # Object  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__series_block, _invalid_mul,     _invalid_mul,     _invalid_mul],   # Block  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__dataframe_dataframe, _invalid_mul,     _mul__series_dataframe, _invalid_mul,     _invalid_mul,     _invalid_mul],   # DataFrame  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__range_range, _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul],   # Range  
        [_invalid_mul,     _invalid_mul,     _mul__int_series, _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__series_series, _invalid_mul,     _invalid_mul,     _invalid_mul],   # Series  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__set_set,    _invalid_mul,     _invalid_mul],   # Set  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__list_list,  _mul__list_list],   # list  
        [_invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _invalid_mul,     _mul__list_list,  _mul__list_list],   # ndarray  
    
        ],
    TK.MOD: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # any  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # none  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__object_int, _invalid_mod,     _mod__dataframe_int, _invalid_mod,     _mod__dataframe_int, _invalid_mod,     _mod__list_int,   _mod__list_int],   # int  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__object_int, _invalid_mod,     _mod__dataframe_int, _invalid_mod,     _mod__dataframe_int, _invalid_mod,     _mod__list_int,   _mod__list_int],   # float  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # bool  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # str  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # datetime  
        [_mod__any_any,    _invalid_mod,     _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # timedelta  
        [_mod__any_any,    _invalid_mod,     _mod__int_object, _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__any_any,    _mod__object_object, _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Object  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Block  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__dataframe_dataframe, _invalid_mod,     _mod__series_dataframe, _invalid_mod,     _invalid_mod,     _invalid_mod],   # DataFrame  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__range_range, _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod],   # Range  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__series_series, _invalid_mod,     _invalid_mod,     _invalid_mod],   # Series  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__set_set,    _invalid_mod,     _invalid_mod],   # Set  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__list_list,  _mod__list_list],   # list  
        [_invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _invalid_mod,     _mod__list_list,  _mod__list_list],   # ndarray  
    
        ],
}
