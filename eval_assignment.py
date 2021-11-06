from conversion import c_box, c_to_bool, c_to_int, c_unbox
from environment import Environment
from exceptions import runtime_error
from tokens import TK


# --------------------------------------------------------------------------------------------------
# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py
# --------------------------------------------------------------------------------------------------


_SUPPORTED_ASSIGN_OPERATIONS = [
    TK.ASSIGN, 
]

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
# referenced in evaluate:
_SUPPORTED_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'object', 'block']
_SUPPORTED_ASSIGNMENT_TOKENS = [TK.APPLY, TK.ASSIGN, TK.DEFINE]


# --------------------------------------------------
#             D I S P A T C H   C O R E 
# --------------------------------------------------


def eval_assign_dispatch(node, left, right):
    l_value = left
    l_ty = type(l_value).__name__
    if getattr(left, 'value', False) or l_ty in ['Int', 'Bool', 'Str', 'Float']:
        l_value = left.value
        l_ty = type(l_value).__name__
    r_value = right
    r_ty = type(r_value).__name__
    if getattr(right, 'value', False) or r_ty in ['Int', 'Bool', 'Str', 'Float']:
        r_value = right.value
        r_ty = type(r_value).__name__
    if l_ty == 'Ident':
        l_value = Environment.current.scope.find(left.token).value
    if r_ty == 'Ident':
        r_value = Environment.current.scope.find(right.token).value
    if l_value is None or r_value is None:
        return None
    return eval_assign_dispatch2(node.token.id, l_value, r_value)


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
    l_value = r_value
    return l_value


def _assign__object_any(l_value, r_value):
    l_value = c_unbox(r_value)
    return l_value


def _assign__any_object(l_value, r_value):
    l_value = r_value.value
    return l_value


def _assign__object_object(l_value, r_value):
    l_value.from_object(r_value)
    return l_value


def _assign__block_object(l_value, r_value):
    l_value = l_value.from_block(r_value)
    return l_value


def _assign__object_block(l_value, r_value):
    l_value = r_value.from_block(l_value)
    return l_value


# --------------------------------------------------
#           E R R O R   F U N C T I O N S 
# --------------------------------------------------


def _invalid_assign(left, right):
    runtime_error(f'Type mismatch for operator assign({type(left)}, {type(right)})', loc=None)


# --------------------------------------------------
#            D I S P A T C H   T A B L E 
# --------------------------------------------------
_assign_dispatch_table = {
    TK.ASSIGN: [
        #          any                     int                    float                    bool                    str                  timedelta                 Object                  Block          
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__object_any,    _invalid_assign],   # any      
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _invalid_assign,        _invalid_assign],   # int      
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _invalid_assign,        _invalid_assign],   # float      
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _invalid_assign,        _invalid_assign],   # bool      
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _invalid_assign,        _assign__any_any,       _invalid_assign,        _invalid_assign,        _invalid_assign],   # str      
        [_assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _assign__any_any,       _invalid_assign,        _invalid_assign],   # timedelta      
        [_assign__any_object,    _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__object_object, _assign__block_object],   # Object      
        [_invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _invalid_assign,        _assign__object_block,  _assign__any_any],   # Block      
    
    ],
}
