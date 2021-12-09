from runtime.conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from runtime.environment import Environment
from runtime.exceptions import runtime_error
from runtime.token_ids import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_ASSIGN_TOKENS = [
    TK.APPLY, 
    TK.ASSIGN, 
    TK.DEFINE, 
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
# referenced in evaluate:
_SUPPORTED_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'object', 'block']
_SUPPORTED_ASSIGNMENT_TOKENS = [TK.APPLY, TK.ASSIGN, TK.DEFINE]


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_assign_dispatch(node, left, right):
    l_value = left
    l_ty = _type2native[type(l_value).__name__]
    if l_ty != 'Object':    # for assignment, left is a ref not a value
        if hasattr(left, 'value'):
            l_value = left.value
        l_ty = _type2native[type(l_value).__name__]
    r_value = right
    if hasattr(right, 'value'):
        r_value = right.value
    r_ty = _type2native[type(r_value).__name__]
    return eval_assign_dispatch2(node.op, l_value, r_value, l_ty, r_ty)


def eval_assign_dispatch2(tkid, l_value, r_value, l_ty=None, r_ty=None):
    if l_ty in _type2idx and r_ty in _type2idx:
        ixl = _type2idx[l_ty]
        ixr = _type2idx[r_ty]
        fn = _assign_dispatch_table[tkid][ixr][ixl]
        return fn(l_value, r_value)


# --------------------------------------------------
#        O P E R A T O R   F U N C T I O N S 
# --------------------------------------------------


def _apply__any_any(l_value, r_value):
    c_box(l_value, c_unbox(r_value))
    return l_value


def _apply__int_any(l_value, r_value):
    l_value = r_value
    return l_value


def _apply__any_datetime(l_value, r_value):
    c_box(l_value, r_value)
    return l_value


def _apply__object_datetime(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _apply__block_datetime(l_value, r_value):
    l_value.from_block(r_value)
    return l_value


def _assign__any_any(l_value, r_value):
    c_box(l_value, c_unbox(r_value))
    return l_value


def _assign__int_any(l_value, r_value):
    l_value = r_value
    return l_value


def _assign__any_datetime(l_value, r_value):
    c_box(l_value, r_value)
    return l_value


def _assign__object_datetime(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _assign__block_datetime(l_value, r_value):
    l_value.from_block(r_value)
    return l_value


def _define__any_any(l_value, r_value):
    c_box(l_value, c_unbox(r_value))
    return l_value


def _define__int_any(l_value, r_value):
    l_value = r_value
    return l_value


def _define__any_datetime(l_value, r_value):
    c_box(l_value, r_value)
    return l_value


def _define__object_datetime(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _define__block_datetime(l_value, r_value):
    l_value.from_block(r_value)
    return l_value


# --------------------------------------------------
#           E R R O R   F U N C T I O N S 
# --------------------------------------------------


def _invalid_apply(left, right):
    runtime_error(f'Type mismatch for operator apply({type(left)}, {type(right)})', loc=None)


def _invalid_assign(left, right):
    runtime_error(f'Type mismatch for operator assign({type(left)}, {type(right)})', loc=None)


def _invalid_define(left, right):
    runtime_error(f'Type mismatch for operator define({type(left)}, {type(right)})', loc=None)


# --------------------------------------------------
#            D I S P A T C H   T A B L E 
# --------------------------------------------------
_assign_dispatch_table = {
    TK.APPLY: [
        # any                     none                    int                     float                   bool                    str                     datetime                timedelta               object                  block                   dataframe               range                   series                  set                     list                    ndarray                 function                
        [_apply__any_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # any  
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # none  
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # int  
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # float  
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # bool  
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # str  
        [_apply__any_datetime,   _invalid_apply,         _apply__any_datetime,   _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__object_datetime, _apply__block_datetime, _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # datetime  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__block_datetime, _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # timedelta  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # Object  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # Block  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # DataFrame  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # Range  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # Series  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply],   # Set  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _apply__int_any,        _invalid_apply],   # list  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _apply__int_any,        _invalid_apply],   # ndarray  
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # function  
    
        ],
    TK.ASSIGN: [
        # any                     none                    int                     float                   bool                    str                     datetime                timedelta               object                  block                   dataframe               range                   series                  set                     list                    ndarray                 function                
        [_assign__any_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # any  
        [_assign__int_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # none  
        [_assign__int_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # int  
        [_assign__int_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # float  
        [_assign__int_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # bool  
        [_assign__int_any,       _invalid_assign,        _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # str  
        [_assign__any_datetime,  _invalid_assign,        _assign__any_datetime,  _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__object_datetime, _assign__block_datetime, _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # datetime  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__block_datetime, _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # timedelta  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Object  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Block  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # DataFrame  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Range  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Series  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign],   # Set  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _assign__int_any,       _invalid_assign],   # list  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _assign__int_any,       _invalid_assign],   # ndarray  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # function  
    
        ],
    TK.DEFINE: [
        # any                     none                    int                     float                   bool                    str                     datetime                timedelta               object                  block                   dataframe               range                   series                  set                     list                    ndarray                 function                
        [_define__any_any,       _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # any  
        [_define__int_any,       _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # none  
        [_define__int_any,       _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # int  
        [_define__int_any,       _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # float  
        [_define__int_any,       _invalid_define,        _define__int_any,       _define__int_any,       _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # bool  
        [_define__int_any,       _invalid_define,        _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # str  
        [_define__any_datetime,  _invalid_define,        _define__any_datetime,  _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__object_datetime, _define__block_datetime, _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # datetime  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__block_datetime, _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # timedelta  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Object  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Block  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # DataFrame  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Range  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Series  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define],   # Set  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _define__int_any,       _invalid_define],   # list  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _define__int_any,       _invalid_define],   # ndarray  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # function  
    
        ],
}
