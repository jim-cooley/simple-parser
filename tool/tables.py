from runtime.token_ids import TK

# --------------------------------------------------
#                    T A B L E S 
# --------------------------------------------------
# 'any' is used to denote the generic routine instead of everything ending up appearing as an int_ conversion

# abbreviations in table:
#   l = l_value    2i: = c_to_int   2f: = c_to_float    u: = unbox      .o = l.from_object( )
#   r = r_value    2b: = c_to_bool  2d: = c_to_dur      b: = box        .b = .from_block( )
#                                                       s: = f'{ }'     .v = .value =
#
#
#   B = TK.BOOL     D = TK.DUR       F = TK.FLOT        I = TK.INT      L = TK.LIST     O = TK.OBJECT   S = TK.STR


# --------------------------------------------------
#         A S S I G N M E N T   T A B L E S 
# --------------------------------------------------
_assign_obj_fn = {
    TK.ASSIGN: [
        #    any         int        float        bool               str      timedelta          Object      Block
        ["b:l,u:r",    "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # any      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # int
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # float
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # bool
        ["l=r",        "l=r",        "l=r",        "invalid",    "l=r",        "invalid",    "b:l,u:r",    "invalid"],   # str
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # timedelta
        ["b:l,r",      "b:l,r",      "invalid",    "invalid",    "invalid",    "invalid",    "l.o",        "l.b"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l.b",        "l=r"],   # Block      
    
    ],
    TK.DEFINE: [
        #    any         int        float        bool               str      timedelta          Object      Block
        ["b:l,u:r",    "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # any      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # int
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # float
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # bool
        ["l=r",        "l=r",        "l=r",        "invalid",    "l=r",        "invalid",    "b:l,u:r",    "invalid"],   # str
        ["l=r",        "invalid",    "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid"],   # timedelta
        ["b:l,r",      "b:l,r",      "invalid",    "invalid",    "invalid",    "invalid",    "l.o",        "l.b"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l.b",        "l=r"],   # Block      
    
    ],
}


# --------------------------------------------------
#         B I N A R Y   O P E R A T I O N S 
# --------------------------------------------------
_evaluate_binops_fn = {
    TK.ADD: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid"],   # any      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "u:l + r",    "invalid"],   # int      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid"],   # float      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid"],   # bool      
        ["s:l + r",    "l + r",      "l + r",      "s:l + r",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid"],   # timedelta      
        ["l + r",      "l + u:r",    "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.SUB: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # any      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "u:l - r",    "invalid"],   # int      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # float      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l - r",      "l - r",      "invalid"],   # str      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # timedelta      
        ["l - r",      "l - u:r",    "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.DIV: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # any      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "u:l / r",    "invalid"],   # int      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # float      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l / r",      "l / r",      "invalid"],   # str      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # timedelta      
        ["l / r",      "l / u:r",    "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.IDIV: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # any      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "u:l // r",   "invalid"],   # int      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # float      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l // r",     "l // r",     "invalid"],   # str      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # timedelta      
        ["l // r",     "l // u:r",   "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.POW: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # any      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "u:l ** r",   "invalid"],   # int      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # float      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l ** r",     "l ** r",     "invalid"],   # str      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # timedelta      
        ["l ** r",     "l ** u:r",   "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.MUL: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid"],   # any      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "u:l * r",    "invalid"],   # int      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid"],   # float      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # bool      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # str      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # timedelta      
        ["l * r",      "l * u:r",    "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
    
    ],
    TK.MOD: [
        #    any         int        float        bool        str      timedelta     Object      Block    
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # any      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "u:l % r",    "invalid"],   # int      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # float      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # bool      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # str      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # timedelta      
        ["l % r",      "l % u:r",    "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid"],   # Object      
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
        ["X",            "X",            "X",            "X",            "X",            "X",            "X",            "X"],   # Object      
    
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
        ["l == r",       "l == r",       "l == r",       "2i:l == r",    "2i:l == r",    "l == r",       "l == r",       "invalid"],   # int
        ["l == r",       "l == r",       "l == r",       "2f:l == r",    "2f:l == r",    "l == r",       "l == r",       "invalid"],   # float
        ["l == r",       "l == 2i:r",    "l == 2f:r",    "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # bool
        ["l == 2i:r",    "l == 2i:r",    "l == 2f:r",    "l == 2b:r",    "l == r",       "l == 2d:r",    "l == r",       "invalid"],   # str
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # timedelta      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.NEQ: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # any      
        ["l != r",       "l != r",       "l != r",       "2i:l != r",    "2i:l != r",    "l != r",       "l != r",       "invalid"],   # int
        ["l != r",       "l != r",       "l != r",       "2i:l != r",    "2f:l != r",    "l != r",       "l != r",       "invalid"],   # float
        ["l != r",       "l != 2i:r",    "l != 2i:r",    "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # bool
        ["l != 2i:r",    "l != 2i:r",    "l != 2f:r",    "l != 2b:r",    "l != r",       "l != 2d:r",    "l != r",       "invalid"],   # str
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # timedelta      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.GTR: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # any      
        ["l > r",        "l > r",        "l > r",        "2i:l > r",     "2i:l > r",     "l > r",        "l > r",        "invalid"],   # int
        ["l > r",        "l > r",        "l > r",        "2i:l > r",     "2f:l > r",     "l > r",        "l > r",        "invalid"],   # float
        ["l > r",        "l > 2i:r",     "l > 2i:r",     "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # bool
        ["l > 2i:r",     "l > 2i:r",     "l > 2f:r",     "l > 2b:r",     "l > r",        "l > 2d:r",     "l > r",        "invalid"],   # str
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # timedelta      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.LESS: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # any      
        ["l < r",        "l < r",        "l < r",        "2i:l < r",     "2i:l < r",     "l < r",        "l < r",        "invalid"],   # int
        ["l < r",        "l < r",        "l < r",        "2i:l < r",     "2f:l < r",     "l < r",        "l < r",        "invalid"],   # float
        ["l < r",        "l < 2i:r",     "l < 2i:r",     "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # bool
        ["l < 2i:r",     "l < 2i:r",     "l < 2f:r",     "l < 2b:r",     "l < r",        "l < 2d:r",     "l < r",        "invalid"],   # str
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # timedelta      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.GTE: [
        #     any           int          float          bool          str                timedelta       Object        Block
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # any      
        ["l >= r",       "l >= r",       "l >= r",       "2i:l >= r",    "2i:l >= r",    "l >= r",       "l >= r",       "invalid"],   # int
        ["l >= r",       "l >= r",       "l >= r",       "2i:l >= r",    "2f:l >= r",    "l >= r",       "l >= r",       "invalid"],   # float
        ["l >= r",       "l >= 2i:r",    "l >= 2i:r",    "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # bool
        ["l >= 2i:r",    "l >= 2i:r",    "l >= 2f:r",    "l >= 2b:r",    "l >= r",       "l >= 2d:r",    "l >= r",       "invalid"],   # str
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # timedelta      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
    TK.LTE: [
        #     any           int          float          bool          str        timedelta       Object        Block     
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # any      
        ["l <= r",       "l <= r",       "l <= r",       "2i:l <= r",    "2i:l <= r",    "l <= r",       "l <= r",       "invalid"],   # int
        ["l <= r",       "l <= r",       "l <= r",       "2i:l <= r",    "2f:l <= r",    "l <= r",       "l <= r",       "invalid"],   # float
        ["l <= r",       "l <= 2i:r",    "l <= 2i:r",    "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # bool
        ["l <= 2i:r",    "l <= 2i:r",    "l <= 2f:r",    "l <= 2b:r",    "l <= r",       "l <= 2d:r",    "l <= r",       "invalid"],   # str
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # timedelta
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
    
    ],
}
