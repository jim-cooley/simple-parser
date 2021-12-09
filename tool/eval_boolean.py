from runtime.conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from runtime.environment import Environment
from runtime.exceptions import runtime_error
from runtime.token_ids import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_BOOLEAN_TOKENS = [
    TK.AND, 
    TK.OR, 
    TK.ISEQ, 
    TK.NEQ, 
    TK.GTR, 
    TK.LESS, 
    TK.GTE, 
    TK.LTE, 
]

_INTRINSIC_VALUE_TYPES = ['any', 'none', 'int', 'float', 'bool', 'str', 'datetime', 'timedelta', 'Object', 'Block', 'DataFrame', 'Range', 'Series', 'Set', 'list', 'ndarray', 'function']

_type2native = {
    'Block': 'block',
    'Bool': 'bool',
    'bool': 'bool',
    'DataFrame': 'dataframe',
    'datafrane': 'dataframe',
    'DateTime': 'datetime',
    'datetime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'float': 'float',
    'Function': 'function',
    'function': 'function',
    'Ident': 'object',
    'Int': 'int',
    'IntrinsicFunction': 'function',
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
    'datafrane': 10,
    'DateTime': 6,
    'datetime': 6,
    'Duration': 7,
    'Float': 3,
    'float': 3,
    'Function': 16,
    'function': 16,
    'Ident': 8,
    'Int': 2,
    'IntrinsicFunction': 16,
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


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_boolean_dispatch(node, left, right):
    l_value = left
    if hasattr(left, 'value'):
        l_value = left.value
    l_ty = _type2native[type(l_value).__name__]
    r_value = right
    if hasattr(right, 'value'):
        r_value = right.value
    r_ty = _type2native[type(r_value).__name__]
    return eval_boolean_dispatch2(node.op, l_value, r_value, l_ty, r_ty)


def eval_boolean_dispatch2(tkid, l_value, r_value, l_ty=None, r_ty=None):
    if l_ty in _type2idx and r_ty in _type2idx:
        ixl = _type2idx[l_ty]
        ixr = _type2idx[r_ty]
        fn = _boolean_dispatch_table[tkid][ixr][ixl]
        return fn(l_value, r_value)


# --------------------------------------------------
#        O P E R A T O R   F U N C T I O N S 
# --------------------------------------------------


def _and__any_any(l_value, r_value):
    return l_value and r_value


def _and__object_timedelta(l_value, r_value):
    return and_tdtd


def _and__object_object(l_value, r_value):
    return and_oo


def _and__dataframe_dataframe(l_value, r_value):
    return pd_and_df


def _and__range_range(l_value, r_value):
    return and_rr


def _and__series_series(l_value, r_value):
    return and_ss


def _and__set_set(l_value, r_value):
    return and_stst


def _and__list_list(l_value, r_value):
    return and_ll


def _or__any_any(l_value, r_value):
    return l_value or r_value


def _or__object_timedelta(l_value, r_value):
    return or_oo


def _or__dataframe_dataframe(l_value, r_value):
    return pd_or_df


def _or__series_series(l_value, r_value):
    return or_ss


def _or__set_set(l_value, r_value):
    return or_stst


def _or__list_list(l_value, r_value):
    return or_ll


def _iseq__any_any(l_value, r_value):
    return l_value == r_value


def _iseq__dataframe_any(l_value, r_value):
    return pd_eq_dfr


def _iseq__bool_int(l_value, r_value):
    return c_to_float(l_value, TK.BOOL) == r_value


def _iseq__str_int(l_value, r_value):
    return c_to_float(l_value, TK.STR) == r_value


def _iseq__int_float(l_value, r_value):
    return l_value == c_to_int(r_value, TK.FLOT)


def _iseq__float_float(l_value, r_value):
    return l_value == c_to_float(r_value, TK.FLOT)


def _iseq__any_bool(l_value, r_value):
    return l_value == c_to_int(r_value, TK.BOOL)


def _iseq__float_bool(l_value, r_value):
    return l_value == c_to_float(r_value, TK.BOOL)


def _iseq__bool_bool(l_value, r_value):
    return l_value == c_to_bool(r_value, TK.BOOL)


def _iseq__datetime_bool(l_value, r_value):
    return l_value == c_to_dur(r_value, TK.BOOL)


def _iseq__object_object(l_value, r_value):
    return ideq_oo


def _iseq__any_dataframe(l_value, r_value):
    return pd_eq_df


def _iseq__range_range(l_value, r_value):
    return iseq_rr


def _iseq__series_series(l_value, r_value):
    return iseq_ss


def _iseq__set_set(l_value, r_value):
    return iseq_stst


def _iseq__list_list(l_value, r_value):
    return iseq_ll


def _neq__any_any(l_value, r_value):
    return l_value != r_value


def _neq__dataframe_any(l_value, r_value):
    return pd_neq_dfr


def _neq__int_float(l_value, r_value):
    return l_value != c_to_int(r_value, TK.FLOT)


def _neq__any_bool(l_value, r_value):
    return l_value != c_to_int(r_value, TK.BOOL)


def _neq__float_bool(l_value, r_value):
    return l_value != c_to_float(r_value, TK.BOOL)


def _neq__bool_bool(l_value, r_value):
    return l_value != c_to_bool(r_value, TK.BOOL)


def _neq__datetime_bool(l_value, r_value):
    return l_value != c_to_dur(r_value, TK.BOOL)


def _neq__object_object(l_value, r_value):
    return neq_oo


def _neq__any_dataframe(l_value, r_value):
    return pd_neq_df


def _neq__range_range(l_value, r_value):
    return neq_rr


def _neq__series_series(l_value, r_value):
    return neq_ss


def _neq__set_set(l_value, r_value):
    return meq_stst


def _neq__list_list(l_value, r_value):
    return neq_ll


def _gtr__any_any(l_value, r_value):
    return l_value > r_value


def _gtr__dataframe_any(l_value, r_value):
    return pd_gtr_dfr


def _gtr__int_float(l_value, r_value):
    return l_value > c_to_int(r_value, TK.FLOT)


def _gtr__any_bool(l_value, r_value):
    return l_value > c_to_int(r_value, TK.BOOL)


def _gtr__float_bool(l_value, r_value):
    return l_value > c_to_float(r_value, TK.BOOL)


def _gtr__bool_bool(l_value, r_value):
    return l_value > c_to_bool(r_value, TK.BOOL)


def _gtr__datetime_bool(l_value, r_value):
    return l_value > c_to_dur(r_value, TK.BOOL)


def _gtr__object_object(l_value, r_value):
    return isgt_oo


def _gtr__any_dataframe(l_value, r_value):
    return pd_gtr_df


def _gtr__range_range(l_value, r_value):
    return isgt_rr


def _gtr__series_series(l_value, r_value):
    return isgt_ss


def _gtr__set_set(l_value, r_value):
    return isgt_stst


def _gtr__list_list(l_value, r_value):
    return isgt_ll


def _less__any_any(l_value, r_value):
    return l_value < r_value


def _less__dataframe_any(l_value, r_value):
    return pd_less_dfr


def _less__int_float(l_value, r_value):
    return l_value < c_to_int(r_value, TK.FLOT)


def _less__any_bool(l_value, r_value):
    return l_value < c_to_int(r_value, TK.BOOL)


def _less__float_bool(l_value, r_value):
    return l_value < c_to_float(r_value, TK.BOOL)


def _less__bool_bool(l_value, r_value):
    return l_value < c_to_bool(r_value, TK.BOOL)


def _less__datetime_bool(l_value, r_value):
    return l_value < c_to_dur(r_value, TK.BOOL)


def _less__object_object(l_value, r_value):
    return islt_oo


def _less__any_dataframe(l_value, r_value):
    return pd_less_df


def _less__range_range(l_value, r_value):
    return islt_rr


def _less__series_series(l_value, r_value):
    return islt_stst


def _less__set_set(l_value, r_value):
    return islt_ss


def _less__list_list(l_value, r_value):
    return islt_ll


def _gte__any_any(l_value, r_value):
    return l_value >= r_value


def _gte__dataframe_any(l_value, r_value):
    return pd_gte_dfr


def _gte__int_float(l_value, r_value):
    return l_value >= c_to_int(r_value, TK.FLOT)


def _gte__any_bool(l_value, r_value):
    return l_value >= c_to_int(r_value, TK.BOOL)


def _gte__float_bool(l_value, r_value):
    return l_value >= c_to_float(r_value, TK.BOOL)


def _gte__bool_bool(l_value, r_value):
    return l_value >= c_to_bool(r_value, TK.BOOL)


def _gte__datetime_bool(l_value, r_value):
    return l_value >= c_to_dur(r_value, TK.BOOL)


def _gte__object_object(l_value, r_value):
    return isgte_oo


def _gte__any_dataframe(l_value, r_value):
    return pd_gte_df


def _gte__range_range(l_value, r_value):
    return isgte_rr


def _gte__series_series(l_value, r_value):
    return isgte_ss


def _gte__set_set(l_value, r_value):
    return is_lte_stst


def _gte__list_list(l_value, r_value):
    return isgte_ll


def _lte__any_any(l_value, r_value):
    return l_value <= r_value


def _lte__dataframe_any(l_value, r_value):
    return pd_lte_dfr


def _lte__int_float(l_value, r_value):
    return l_value <= c_to_int(r_value, TK.FLOT)


def _lte__any_bool(l_value, r_value):
    return l_value <= c_to_int(r_value, TK.BOOL)


def _lte__float_bool(l_value, r_value):
    return l_value <= c_to_float(r_value, TK.BOOL)


def _lte__bool_bool(l_value, r_value):
    return l_value <= c_to_bool(r_value, TK.BOOL)


def _lte__datetime_bool(l_value, r_value):
    return l_value <= c_to_dur(r_value, TK.BOOL)


def _lte__object_object(l_value, r_value):
    return isgte_oo


def _lte__any_dataframe(l_value, r_value):
    return pd_lte_df


def _lte__range_range(l_value, r_value):
    return islte_rr


def _lte__series_series(l_value, r_value):
    return islte_ss


def _lte__set_set(l_value, r_value):
    return is_lte_stst


def _lte__list_list(l_value, r_value):
    return islte_ll


# --------------------------------------------------
#           E R R O R   F U N C T I O N S 
# --------------------------------------------------


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
_boolean_dispatch_table = {
    TK.AND: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # any  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # none  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # int  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # float  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # bool  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # str  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # datetime  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__object_timedelta, _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # timedelta  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__object_object, _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Object  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Block  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__dataframe_dataframe, _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # DataFrame  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__range_range, _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Range  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__series_series, _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Series  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__set_set,    _invalid_and,     _invalid_and,     _invalid_and],   # Set  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__list_list,  _and__list_list,  _invalid_and],   # list  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__list_list,  _and__list_list,  _invalid_and],   # ndarray  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # function  
    
        ],
    TK.OR: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # any  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # none  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # int  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # float  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # bool  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # str  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # datetime  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__object_timedelta, _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # timedelta  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Object  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Block  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__dataframe_dataframe, _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # DataFrame  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Range  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__series_series, _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Series  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__set_set,     _invalid_or,      _invalid_or,      _invalid_or],   # Set  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__list_list,   _or__list_list,   _invalid_or],   # list  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__list_list,   _or__list_list,   _invalid_or],   # ndarray  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # function  
    
        ],
    TK.ISEQ: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _iseq__dataframe_any, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # any  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # none  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__bool_int,  _iseq__str_int,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _iseq__dataframe_any, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # int  
        [_iseq__any_any,   _iseq__any_any,   _iseq__int_float, _iseq__float_float, _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _iseq__dataframe_any, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # float  
        [_iseq__any_bool,  _iseq__any_bool,  _iseq__any_bool,  _iseq__float_bool, _iseq__bool_bool, _iseq__any_any,   _iseq__datetime_bool, _iseq__datetime_bool, _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # bool  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # str  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # datetime  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # timedelta  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__object_object, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Object  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Block  
        [_iseq__any_dataframe, _invalid_iseq,    _iseq__any_dataframe, _iseq__any_dataframe, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__any_dataframe, _invalid_iseq,    _iseq__any_dataframe, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # DataFrame  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__range_range, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Range  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__dataframe_any, _invalid_iseq,    _iseq__series_series, _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Series  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__set_set,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Set  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__list_list, _iseq__list_list, _invalid_iseq],   # list  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__list_list, _iseq__list_list, _invalid_iseq],   # ndarray  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # function  
    
        ],
    TK.NEQ: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _neq__dataframe_any, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # any  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # none  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _neq__dataframe_any, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # int  
        [_neq__any_any,    _neq__any_any,    _neq__int_float,  _neq__int_float,  _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _neq__dataframe_any, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # float  
        [_neq__any_bool,   _neq__any_bool,   _neq__any_bool,   _neq__float_bool, _neq__bool_bool,  _neq__any_any,    _neq__datetime_bool, _neq__datetime_bool, _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # bool  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # str  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # datetime  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # timedelta  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__object_object, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Object  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Block  
        [_neq__any_dataframe, _invalid_neq,     _neq__any_dataframe, _neq__any_dataframe, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__any_dataframe, _invalid_neq,     _neq__any_dataframe, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # DataFrame  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__range_range, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Range  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__dataframe_any, _invalid_neq,     _neq__series_series, _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Series  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__set_set,    _invalid_neq,     _invalid_neq,     _invalid_neq],   # Set  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__list_list,  _neq__list_list,  _invalid_neq],   # list  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__list_list,  _neq__list_list,  _invalid_neq],   # ndarray  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # function  
    
        ],
    TK.GTR: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _gtr__dataframe_any, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # any  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # none  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _gtr__dataframe_any, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # int  
        [_gtr__any_any,    _gtr__any_any,    _gtr__int_float,  _gtr__int_float,  _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _gtr__dataframe_any, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # float  
        [_gtr__any_bool,   _gtr__any_bool,   _gtr__any_bool,   _gtr__float_bool, _gtr__bool_bool,  _gtr__any_any,    _gtr__datetime_bool, _gtr__datetime_bool, _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # bool  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # str  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # datetime  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # timedelta  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__object_object, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Object  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Block  
        [_gtr__any_dataframe, _invalid_gtr,     _gtr__any_dataframe, _gtr__any_dataframe, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__any_dataframe, _invalid_gtr,     _gtr__any_dataframe, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # DataFrame  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__range_range, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Range  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__dataframe_any, _invalid_gtr,     _gtr__series_series, _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Series  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__set_set,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Set  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__list_list,  _gtr__list_list,  _invalid_gtr],   # list  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__list_list,  _gtr__list_list,  _invalid_gtr],   # ndarray  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # function  
    
        ],
    TK.LESS: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _less__dataframe_any, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # any  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # none  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _less__dataframe_any, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # int  
        [_less__any_any,   _less__any_any,   _less__int_float, _less__int_float, _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _less__dataframe_any, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # float  
        [_less__any_bool,  _less__any_bool,  _less__any_bool,  _less__float_bool, _less__bool_bool, _less__any_any,   _less__datetime_bool, _less__datetime_bool, _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # bool  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # str  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # datetime  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # timedelta  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__object_object, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Object  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Block  
        [_less__any_dataframe, _invalid_less,    _less__any_dataframe, _less__any_dataframe, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__any_dataframe, _invalid_less,    _less__any_dataframe, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # DataFrame  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__range_range, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Range  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__dataframe_any, _invalid_less,    _less__series_series, _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Series  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__set_set,   _invalid_less,    _invalid_less,    _invalid_less],   # Set  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__list_list, _less__list_list, _invalid_less],   # list  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__list_list, _less__list_list, _invalid_less],   # ndarray  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # function  
    
        ],
    TK.GTE: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _gte__dataframe_any, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # any  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # none  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _gte__dataframe_any, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # int  
        [_gte__any_any,    _gte__any_any,    _gte__int_float,  _gte__int_float,  _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _gte__dataframe_any, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # float  
        [_gte__any_bool,   _gte__any_bool,   _gte__any_bool,   _gte__float_bool, _gte__bool_bool,  _gte__any_any,    _gte__datetime_bool, _gte__datetime_bool, _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # bool  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # str  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # datetime  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # timedelta  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__object_object, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Object  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Block  
        [_gte__any_dataframe, _invalid_gte,     _gte__any_dataframe, _gte__any_dataframe, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__any_dataframe, _invalid_gte,     _gte__any_dataframe, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # DataFrame  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__range_range, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Range  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__dataframe_any, _invalid_gte,     _gte__series_series, _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Series  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__set_set,    _invalid_gte,     _invalid_gte,     _invalid_gte],   # Set  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__list_list,  _gte__list_list,  _invalid_gte],   # list  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__list_list,  _gte__list_list,  _invalid_gte],   # ndarray  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # function  
    
        ],
    TK.LTE: [
        # any               none              int               float             bool              str               datetime          timedelta         object            block             dataframe         range             series            set               list              ndarray           function          
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _lte__dataframe_any, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # any  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # none  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _lte__dataframe_any, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # int  
        [_lte__any_any,    _lte__any_any,    _lte__int_float,  _lte__int_float,  _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _lte__dataframe_any, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # float  
        [_lte__any_bool,   _lte__any_bool,   _lte__any_bool,   _lte__float_bool, _lte__bool_bool,  _lte__any_any,    _lte__datetime_bool, _lte__datetime_bool, _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # bool  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # str  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # datetime  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # timedelta  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__object_object, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Object  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Block  
        [_lte__any_dataframe, _invalid_lte,     _lte__any_dataframe, _lte__any_dataframe, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__any_dataframe, _invalid_lte,     _lte__any_dataframe, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # DataFrame  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__range_range, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Range  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__dataframe_any, _invalid_lte,     _lte__series_series, _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Series  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__set_set,    _invalid_lte,     _invalid_lte,     _invalid_lte],   # Set  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__list_list,  _lte__list_list,  _invalid_lte],   # list  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__list_list,  _lte__list_list,  _invalid_lte],   # ndarray  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # function  
    
        ],
}
