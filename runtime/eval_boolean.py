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


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_boolean_dispatch(node, left, right):
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
    return eval_boolean_dispatch2(node.op, l_value, r_value)


def eval_boolean_dispatch2(tkid, l_value, r_value):
    l_ty = type(l_value).__name__
    r_ty = type(r_value).__name__
    l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]
    r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]
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


def _and__list_list(l_value, r_value):
    return land(l_value,r_value)


def _or__any_any(l_value, r_value):
    return l_value and r_value


def _or__list_list(l_value, r_value):
    return lor(l_value,r_value)


def _iseq__any_any(l_value, r_value):
    return l_value == r_value


def _iseq__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) == r_value


def _iseq__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) == r_value


def _iseq__bool_float(l_value, r_value):
    return c_to_float(l_value, TK.BOOL) == r_value


def _iseq__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) == r_value


def _iseq__int_bool(l_value, r_value):
    return l_value == c_to_int(r_value, TK.BOOL)


def _iseq__float_bool(l_value, r_value):
    return l_value == c_to_float(r_value, TK.BOOL)


def _iseq__any_str(l_value, r_value):
    return l_value == c_to_int(r_value, TK.STR)


def _iseq__float_str(l_value, r_value):
    return l_value == c_to_float(r_value, TK.STR)


def _iseq__bool_str(l_value, r_value):
    return l_value == c_to_bool(r_value, TK.STR)


def _iseq__timedelta_str(l_value, r_value):
    return l_value == c_to_dur(r_value, TK.STR)


def _iseq__series_series(l_value, r_value):
    return siseq(l_value,r_value)


def _iseq__set_set(l_value, r_value):
    return s2iseq(l_value,r_value)


def _iseq__list_list(l_value, r_value):
    return liseq(l_value,r_value)


def _neq__any_any(l_value, r_value):
    return l_value != r_value


def _neq__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) != r_value


def _neq__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) != r_value


def _neq__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) != r_value


def _neq__int_bool(l_value, r_value):
    return l_value != c_to_int(r_value, TK.BOOL)


def _neq__any_str(l_value, r_value):
    return l_value != c_to_int(r_value, TK.STR)


def _neq__float_str(l_value, r_value):
    return l_value != c_to_float(r_value, TK.STR)


def _neq__bool_str(l_value, r_value):
    return l_value != c_to_bool(r_value, TK.STR)


def _neq__timedelta_str(l_value, r_value):
    return l_value != c_to_dur(r_value, TK.STR)


def _neq__series_series(l_value, r_value):
    return sneq(l_value,r_value)


def _neq__set_set(l_value, r_value):
    return s2neq(l_value,r_value)


def _neq__list_list(l_value, r_value):
    return lneq(l_value,r_value)


def _gtr__any_any(l_value, r_value):
    return l_value > r_value


def _gtr__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) > r_value


def _gtr__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) > r_value


def _gtr__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) > r_value


def _gtr__int_bool(l_value, r_value):
    return l_value > c_to_int(r_value, TK.BOOL)


def _gtr__any_str(l_value, r_value):
    return l_value > c_to_int(r_value, TK.STR)


def _gtr__float_str(l_value, r_value):
    return l_value > c_to_float(r_value, TK.STR)


def _gtr__bool_str(l_value, r_value):
    return l_value > c_to_bool(r_value, TK.STR)


def _gtr__timedelta_str(l_value, r_value):
    return l_value > c_to_dur(r_value, TK.STR)


def _gtr__series_series(l_value, r_value):
    return sgtr(l_value,r_value)


def _gtr__set_set(l_value, r_value):
    return s2gtr(l_value,r_value)


def _gtr__list_list(l_value, r_value):
    return lgtr(l_value,r_value)


def _less__any_any(l_value, r_value):
    return l_value < r_value


def _less__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) < r_value


def _less__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) < r_value


def _less__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) < r_value


def _less__int_bool(l_value, r_value):
    return l_value < c_to_int(r_value, TK.BOOL)


def _less__any_str(l_value, r_value):
    return l_value < c_to_int(r_value, TK.STR)


def _less__float_str(l_value, r_value):
    return l_value < c_to_float(r_value, TK.STR)


def _less__bool_str(l_value, r_value):
    return l_value < c_to_bool(r_value, TK.STR)


def _less__timedelta_str(l_value, r_value):
    return l_value < c_to_dur(r_value, TK.STR)


def _less__series_series(l_value, r_value):
    return sless(l_value,r_value)


def _less__set_set(l_value, r_value):
    return s2less(l_value,r_value)


def _less__list_list(l_value, r_value):
    return lless(l_value,r_value)


def _gte__any_any(l_value, r_value):
    return l_value >= r_value


def _gte__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) >= r_value


def _gte__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) >= r_value


def _gte__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) >= r_value


def _gte__int_bool(l_value, r_value):
    return l_value >= c_to_int(r_value, TK.BOOL)


def _gte__any_str(l_value, r_value):
    return l_value >= c_to_int(r_value, TK.STR)


def _gte__float_str(l_value, r_value):
    return l_value >= c_to_float(r_value, TK.STR)


def _gte__bool_str(l_value, r_value):
    return l_value >= c_to_bool(r_value, TK.STR)


def _gte__timedelta_str(l_value, r_value):
    return l_value >= c_to_dur(r_value, TK.STR)


def _gte__series_series(l_value, r_value):
    return sgte(l_value,r_value)


def _gte__set_set(l_value, r_value):
    return s2gte(l_value,r_value)


def _gte__list_list(l_value, r_value):
    return lgte(l_value,r_value)


def _lte__any_any(l_value, r_value):
    return l_value <= r_value


def _lte__bool_int(l_value, r_value):
    return c_to_int(l_value, TK.BOOL) <= r_value


def _lte__str_int(l_value, r_value):
    return c_to_int(l_value, TK.STR) <= r_value


def _lte__str_float(l_value, r_value):
    return c_to_float(l_value, TK.STR) <= r_value


def _lte__int_bool(l_value, r_value):
    return l_value <= c_to_int(r_value, TK.BOOL)


def _lte__any_str(l_value, r_value):
    return l_value <= c_to_int(r_value, TK.STR)


def _lte__float_str(l_value, r_value):
    return l_value <= c_to_float(r_value, TK.STR)


def _lte__bool_str(l_value, r_value):
    return l_value <= c_to_bool(r_value, TK.STR)


def _lte__timedelta_str(l_value, r_value):
    return l_value <= c_to_dur(r_value, TK.STR)


def _lte__series_series(l_value, r_value):
    return slte(l_value,r_value)


def _lte__set_set(l_value, r_value):
    return s2lte(l_value,r_value)


def _lte__list_list(l_value, r_value):
    return llte(l_value,r_value)


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
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # any  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # int  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # float  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # bool  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # str  
        [_and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _and__any_any,    _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # timedelta  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Object  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Block  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # DataFrame  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Range  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Series  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and],   # Set  
        [_invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _invalid_and,     _and__list_list],   # list  
    
        ],
    TK.OR: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # any  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # int  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # float  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # bool  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # str  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # timedelta  
        [_or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _or__any_any,     _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Object  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Block  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # DataFrame  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Range  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Series  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or],   # Set  
        [_invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _invalid_or,      _or__list_list],   # list  
    
        ],
    TK.ISEQ: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # any  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__bool_int,  _iseq__str_int,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # int  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__bool_float, _iseq__str_float, _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # float  
        [_iseq__any_any,   _iseq__int_bool,  _iseq__float_bool, _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # bool  
        [_iseq__any_str,   _iseq__any_str,   _iseq__float_str, _iseq__bool_str,  _iseq__any_any,   _iseq__timedelta_str, _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # str  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # timedelta  
        [_iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _iseq__any_any,   _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Object  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Block  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # DataFrame  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq],   # Range  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__series_series, _invalid_iseq,    _invalid_iseq],   # Series  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__set_set,   _invalid_iseq],   # Set  
        [_invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _invalid_iseq,    _iseq__list_list],   # list  
    
        ],
    TK.NEQ: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # any  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__bool_int,   _neq__str_int,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # int  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__bool_int,   _neq__str_float,  _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # float  
        [_neq__any_any,    _neq__int_bool,   _neq__int_bool,   _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # bool  
        [_neq__any_str,    _neq__any_str,    _neq__float_str,  _neq__bool_str,   _neq__any_any,    _neq__timedelta_str, _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # str  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # timedelta  
        [_neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _neq__any_any,    _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Object  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Block  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # DataFrame  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq],   # Range  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__series_series, _invalid_neq,     _invalid_neq],   # Series  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__set_set,    _invalid_neq],   # Set  
        [_invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _invalid_neq,     _neq__list_list],   # list  
    
        ],
    TK.GTR: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # any  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__bool_int,   _gtr__str_int,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # int  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__bool_int,   _gtr__str_float,  _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # float  
        [_gtr__any_any,    _gtr__int_bool,   _gtr__int_bool,   _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # bool  
        [_gtr__any_str,    _gtr__any_str,    _gtr__float_str,  _gtr__bool_str,   _gtr__any_any,    _gtr__timedelta_str, _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # str  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # timedelta  
        [_gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _gtr__any_any,    _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Object  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Block  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # DataFrame  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr],   # Range  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__series_series, _invalid_gtr,     _invalid_gtr],   # Series  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__set_set,    _invalid_gtr],   # Set  
        [_invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _invalid_gtr,     _gtr__list_list],   # list  
    
        ],
    TK.LESS: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # any  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__bool_int,  _less__str_int,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # int  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__bool_int,  _less__str_float, _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # float  
        [_less__any_any,   _less__int_bool,  _less__int_bool,  _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # bool  
        [_less__any_str,   _less__any_str,   _less__float_str, _less__bool_str,  _less__any_any,   _less__timedelta_str, _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # str  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # timedelta  
        [_less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _less__any_any,   _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Object  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Block  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # DataFrame  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less],   # Range  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__series_series, _invalid_less,    _invalid_less],   # Series  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__set_set,   _invalid_less],   # Set  
        [_invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _invalid_less,    _less__list_list],   # list  
    
        ],
    TK.GTE: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # any  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__bool_int,   _gte__str_int,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # int  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__bool_int,   _gte__str_float,  _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # float  
        [_gte__any_any,    _gte__int_bool,   _gte__int_bool,   _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # bool  
        [_gte__any_str,    _gte__any_str,    _gte__float_str,  _gte__bool_str,   _gte__any_any,    _gte__timedelta_str, _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # str  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # timedelta  
        [_gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _gte__any_any,    _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Object  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Block  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # DataFrame  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte],   # Range  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__series_series, _invalid_gte,     _invalid_gte],   # Series  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__set_set,    _invalid_gte],   # Set  
        [_invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _invalid_gte,     _gte__list_list],   # list  
    
        ],
    TK.LTE: [
        #       any              int             float            bool             str           timedelta         Object           Block          DataFrame          Range           Series            Set             list      
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # any  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__bool_int,   _lte__str_int,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # int  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__bool_int,   _lte__str_float,  _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # float  
        [_lte__any_any,    _lte__int_bool,   _lte__int_bool,   _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # bool  
        [_lte__any_str,    _lte__any_str,    _lte__float_str,  _lte__bool_str,   _lte__any_any,    _lte__timedelta_str, _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # str  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # timedelta  
        [_lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _lte__any_any,    _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Object  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Block  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # DataFrame  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte],   # Range  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__series_series, _invalid_lte,     _invalid_lte],   # Series  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__set_set,    _invalid_lte],   # Set  
        [_invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _invalid_lte,     _lte__list_list],   # list  
    
        ],
}
