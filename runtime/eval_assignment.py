from runtime.conversion import c_box, c_to_bool, c_to_float, c_to_int, c_unbox
from runtime.environment import Environment
from runtime.exceptions import runtime_error
from runtime.token_ids import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_ASSIGN_TOKENS = [
    TK.ASSIGN, 
    TK.DEFINE, 
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
# referenced in evaluate:
_SUPPORTED_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'object', 'block']
_SUPPORTED_ASSIGNMENT_TOKENS = [TK.APPLY, TK.ASSIGN, TK.DEFINE]


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_assign_dispatch(node, left, right):
    l_value = left
    l_ty = type(l_value).__name__
    if l_ty != 'Object':    # for assignment, left is a ref not a value
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
    return eval_assign_dispatch2(node.op, l_value, r_value)


def eval_assign_dispatch2(tkid, l_value, r_value):
    l_ty = type(l_value).__name__
    r_ty = type(r_value).__name__
    l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]
    r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]
    if l_ty in _type2idx and r_ty in _type2idx:
        ixl = _type2idx[l_ty]
        ixr = _type2idx[r_ty]
        fn = _assign_dispatch_table[tkid][ixr][ixl]
        return fn(l_value, r_value)


# --------------------------------------------------
#        O P E R A T O R   F U N C T I O N S 
# --------------------------------------------------


def _assign__any_any(l_value, r_value):
    c_box(l_value, c_unbox(r_value))
    return l_value


def _assign__int_any(l_value, r_value):
    l_value = r_value
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


def _invalid_assign(left, right):
    runtime_error(f'Type mismatch for operator assign({type(left)}, {type(right)})', loc=None)


def _invalid_define(left, right):
    runtime_error(f'Type mismatch for operator define({type(left)}, {type(right)})', loc=None)


# --------------------------------------------------
#            D I S P A T C H   T A B L E 
# --------------------------------------------------
_assign_dispatch_table = {
    TK.ASSIGN: [
        #          any                    int                   float                  bool                   str                 timedelta               Object                 Block                DataFrame                Range                 Series                  Set                   list         
        [_assign__any_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # any  
        [_assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # int  
        [_assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # float  
        [_assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # bool  
        [_assign__int_any,       _assign__int_any,       _assign__int_any,       _invalid_assign,        _assign__int_any,       _invalid_assign,        _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # str  
        [_assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__int_any,       _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # timedelta  
        [_assign__any_object,    _assign__any_object,    _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__object_object, _assign__block_object,  _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Object  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__block_object,  _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # Block  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign],   # DataFrame  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign,        _invalid_assign],   # Range  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign,        _invalid_assign],   # Series  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any,       _invalid_assign],   # Set  
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__int_any],   # list  
    
        ],
    TK.DEFINE: [
        #          any                    int                   float                  bool                   str                 timedelta               Object                 Block                DataFrame                Range                 Series                  Set                   list         
        [_define__any_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # any  
        [_define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # int  
        [_define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # float  
        [_define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # bool  
        [_define__int_any,       _define__int_any,       _define__int_any,       _invalid_define,        _define__int_any,       _invalid_define,        _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # str  
        [_define__int_any,       _invalid_define,        _define__int_any,       _define__int_any,       _define__int_any,       _define__int_any,       _define__any_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # timedelta  
        [_define__any_object,    _define__any_object,    _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__object_object, _define__block_object,  _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Object  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__block_object,  _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # Block  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define],   # DataFrame  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define,        _invalid_define],   # Range  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define,        _invalid_define],   # Series  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any,       _invalid_define],   # Set  
        [_invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _invalid_define,        _define__int_any],   # list  
    
        ],
}
