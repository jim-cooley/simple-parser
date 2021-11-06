from tokens import TK


# --------------------------------------------------
#                    T A B L E S 
# --------------------------------------------------
# 'any' is used to denote the generic routine instead of everything ending up appearing as an int_ conversion

# abbreviations in table:
#   l = l_value     2i = c_to_int    2f = c_to_float    u = unbox       s( ) = f'{ }'
#   r = r_value     2b = c_to_bool   2d = c_to_dur      b = box         .o( ) = .from_object( )
#                                                                       .b( ) = .from_block( )
#                                                                       v( ) = .value =
#
#   B = TK.BOOL     D = TK.DUR       F = TK.FLOT        I = TK.INT      L = TK.LIST     O = TK.OBJECT   S = TK.STR


# --------------------------------------------------
#         A S S I G N M E N T   T A B L E S 
# --------------------------------------------------
_assign_obj_fn = {
    TK.ASSIGN: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["r",          "r",          "r",          "r",          "r",          "r",          "u(r)",       "invalid"],   # any      
        ["r",          "r",          "r",          "r",          "r",          "r",          "invalid",    "invalid"],   # int      
        ["r",          "r",          "r",          "r",          "r",          "r",          "invalid",    "invalid"],   # float      
        ["r",          "r",          "r",          "r",          "r",          "r",          "invalid",    "invalid"],   # bool      
        ["r",          "r",          "r",          "invalid",    "r",          "invalid",    "invalid",    "invalid"],   # str      
        ["r",          "r",          "r",          "r",          "r",          "r",          "invalid",    "invalid"],   # timedelta      
        [".v(r)",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    ".o(r)",      ".b(r)"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    ".b(r)",      "r"],   # Block      
    
    ],
}


# --------------------------------------------------
#         B I N A R Y   O P E R A T I O N S 
# --------------------------------------------------
_evaluate_binops_fn = {
    TK.ADD: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s(r)",   "l + r",      "l + r",      "invalid"],   # any      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s(r)",   "l + r",      "u(l) + r",   "invalid"],   # int      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s(r)",   "l + r",      "l + r",      "invalid"],   # float      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s(r)",   "l + r",      "l + r",      "invalid"],   # bool      
        ["f'{l}' + r", "s(l) + r",   "s(l) + r",   "s(l) + r",   "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s(r)",   "l + r",      "l + r",      "invalid"],   # timedelta      
        ["l + r",      "l + u(r)",   "l + r",      "l + r",      "l + s(r)",   "l + r",      "l + r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.SUB: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # any      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "u(l) - r",   "invalid"],   # int      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # float      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l - r",      "l - r",      "invalid"],   # str      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # timedelta      
        ["l - r",      "l - u(r)",   "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.DIV: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # any      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "u(l) / r",   "invalid"],   # int      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # float      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l / r",      "l / r",      "invalid"],   # str      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # timedelta      
        ["l / r",      "l / u(r)",   "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.IDIV: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # any      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "u(l) // r",  "invalid"],   # int      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # float      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l // r",     "l // r",     "invalid"],   # str      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # timedelta      
        ["l // r",     "l // u(r)",  "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.POW: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # any      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "u(l) ** r",  "invalid"],   # int      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # float      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l ** r",     "l ** r",     "invalid"],   # str      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # timedelta      
        ["l ** r",     "l ** u(r)",  "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.MUL: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid"],   # any      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "u(l) * r",   "invalid"],   # int      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid"],   # float      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # bool      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # str      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # timedelta      
        ["l * r",      "l * u(r)",   "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.MOD: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # any      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "u(l) % r",   "invalid"],   # int      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # float      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # bool      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # str      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # timedelta      
        ["l % r",      "l % u(r)",   "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
}


# --------------------------------------------------
#        B O O L E A N   O P E R A T I O N S 
# --------------------------------------------------
_evaluate_boolops_fn = {
    TK.AND: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # any      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # int      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # float      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # bool      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # str      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # timedelta      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
    
    ],
    TK.OR: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # any      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # int      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # float      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # bool      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # str      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # timedelta      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.ISEQ: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # any      
        ["l == r",       "l == r",       "l == r",       "l == 2b(r, I)", "l == r",       "l == r",       "l == r",       "invalid"],   # int      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # float      
        ["l == r",       "l == 2i(r, B)", "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # bool      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # str      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # timedelta      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.NEQ: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # any      
        ["l != r",       "l != r",       "l != r",       "l != 2b(r, I)", "l != r",       "l != r",       "l != r",       "invalid"],   # int      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # float      
        ["l != r",       "l != 2i(r, B)", "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # bool      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # str      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # timedelta      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.GTR: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # any      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > 2i(r)",    "l > r",        "l > r",        "invalid"],   # int      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # float      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # bool      
        ["2i(l) > r",    "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # str      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # timedelta      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.LESS: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # any      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # int      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # float      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # bool      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # str      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # timedelta      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.GTE: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # any      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # int      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # float      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # bool      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # str      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # timedelta      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.LTE: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # any      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # int      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # float      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # bool      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # str      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # timedelta      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
}
