from copy import deepcopy

from runtime.conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from runtime.exceptions import runtime_error
from runtime.indexdict import IndexedDict
from runtime.options import getOptions
from runtime.token_ids import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_ASSIGN_TOKENS = [
    TK.ASSIGN, 
    TK.DEFINE, 
]

_INTRINSIC_VALUE_TYPES = ['any', 'none', 'int', 'float', 'bool', 'str', 'datetime', 'timedelta', 'Object', 'Block', 'DataFrame', 'Range', 'Series', 'Set', 'list', 'ndarray', 'function']

_type2native = {
    'Block': 'block',
    'Bool': 'bool',
    'bool': 'bool',
    'DataFrame': 'dataframe',
    'datyaframe': 'dataframe',
    'DateTime': 'datetime',
    'datetime': 'datetime',
    'Duration': 'timedelta',
    'Float': 'float',
    'float': 'float',
    'Function': 'function',
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
    'dataframe': 10,
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
    l_ty = type(l_value).__name__
    if l_ty not in ['Object', 'Function', 'IntrinsicFunction']:    # for assignment, left is a ref not a value
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


def prepare_parameters(fn, args):
    _values = []
    _fields = []
    _defaults = {}
    if hasattr(fn, 'defaults'):
        if fn.defaults is not None:
            _defaults = deepcopy(fn.defaults)
            _fields = list(_defaults.keys())
            _values = list(_defaults.values())
    if args is not None:
        for idx in range(0, len(args)):
            val = args[idx]
            if hasattr(val, 'name'):
                name = val.name
            else:
                name = None
            _resolve(idx, name, c_unbox(val), _fields, _values)
    return IndexedDict(fields=_fields, values=_values)


def _resolve(idx, name, value, fields, values):
    if name is None:
        if idx < len(values):
            values[idx] = value
        else:
            values.append(value)
    else:
        if name in fields:
            slot = fields.index(name)
            values[slot] = value
        else:
            fields.append(name)
            values.append(value)


# --------------------------------------------------
#        O P E R A T O R   F U N C T I O N S 
# --------------------------------------------------
def _apply__any_function(l_value, r_value):
    fn = l_value
    args = prepare_parameters(fn, [r_value])
    options = getOptions('focal')
    focal = options.focal
    return fn.invoke(focal.interpreter, args)


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


def _assign__any_object(l_value, r_value):
    c_box(l_value, r_value)
    return l_value


def _assign__object_object(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _assign__block_object(l_value, r_value):
    l_value.from_block(r_value)
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


def _define__any_any(l_value, r_value):
    c_box(l_value, c_unbox(r_value))
    return l_value


def _define__int_any(l_value, r_value):
    l_value = r_value
    return l_value


def _define__any_object(l_value, r_value):
    c_box(l_value, r_value)
    return l_value


def _define__object_object(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _define__block_object(l_value, r_value):
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
        [_apply__any_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # any
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # none
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # int
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # float
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # bool
        [_apply__int_any,        _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__int_any,        _apply__any_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # str
        [_apply__any_datetime,   _invalid_apply,         _apply__any_datetime,   _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__object_datetime, _apply__block_datetime, _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # datetime
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__block_datetime, _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # timedelta
        [_apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,        _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,         _apply__any_any,      _apply__any_function],   # Object
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # Block
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # DataFrame
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # Range
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_function],   # Series
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _invalid_apply,         _invalid_apply,         _apply__any_function],   # Set
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__any_function],   # list
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__int_any,        _apply__int_any,        _apply__any_function],   # ndarray
        [_invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _apply__any_any,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply,         _invalid_apply],   # function
    
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
