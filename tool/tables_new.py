from tokens import TK


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
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["b:l,u:r",    "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["l=r",        "l=r",        "l=r",        "invalid",    "l=r",        "invalid",    "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["b:l,r",      "b:l,r",      "invalid",    "invalid",    "invalid",    "invalid",    "l.o",        "l.b",        "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l.b",        "l=r",        "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r"],   # list      
    
        ],
    TK.DEFINE: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["b:l,u:r",    "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["l=r",        "l=r",        "l=r",        "invalid",    "l=r",        "invalid",    "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l=r",        "invalid",    "l=r",        "l=r",        "l=r",        "l=r",        "b:l,u:r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["b:l,r",      "b:l,r",      "invalid",    "invalid",    "invalid",    "invalid",    "l.o",        "l.b",        "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l.b",        "l=r",        "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r",        "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l=r"],   # list      
    
        ],
}


# --------------------------------------------------
#         B I N A R Y   O P E R A T I O N S 
# --------------------------------------------------
_evaluate_binops_fn = {
    TK.ADD: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "u:l + r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["s:l + r",    "l + r",      "l + r",      "s:l + r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l + r",      "l + r",      "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l + r",      "l + u:r",    "l + r",      "l + r",      "l + s:r",    "l + r",      "l + r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "sadd(l,r)",  "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2add(1,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "ladd(1,r)"],   # list      
    
        ],
    TK.SUB: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "u:l - r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l - r",      "l - r",      "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l - r",      "l - u:r",    "l - r",      "l - r",      "invalid",    "l - r",      "l - r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "ssub(l,r)",  "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2sub(l,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "lsub(l,r)"],   # list      
    
        ],
    TK.DIV: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "u:l / r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l / r",      "l / r",      "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l / r",      "l / u:r",    "l / r",      "l / r",      "invalid",    "l / r",      "l / r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "sdiv(l,r)",  "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2div(l,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "ldiv(l,r)"],   # list      
    
        ],
    TK.IDIV: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "u:l // r",   "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l // r",     "l // r",     "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l // r",     "l // u:r",   "l // r",     "l // r",     "invalid",    "l // r",     "l // r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "sidiv(l,r)", "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2idiv(l,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "lidiv(l,r)"],   # list      
    
        ],
    TK.POW: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "u:l ** r",   "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l ** r",     "l ** r",     "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l ** r",     "l ** u:r",   "l ** r",     "l ** r",     "invalid",    "l ** r",     "l ** r",     "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # list      
    
        ],
    TK.MUL: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "u:l * r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l * r",      "l * r",      "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l * r",      "l * u:r",    "l * r",      "l * r",      "invalid",    "l * r",      "l * r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "lrmul(l,r)", "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "smul(l,r)",  "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2mul(l,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "lmul(l,r)"],   # list      
    
        ],
    TK.MOD: [
        #     any          int         float         bool          str       timedelta      Object        Block      DataFrame      Range        Series         Set          list     
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # any      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "u:l % r",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # int      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # float      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # bool      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # str      
        ["l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # timedelta      
        ["l % r",      "l % u:r",    "l % r",      "l % r",      "l % r",      "l % r",      "l % r",      "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Object      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Block      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # DataFrame      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid"],   # Range      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "smod(l,r)",  "invalid",    "invalid"],   # Series      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "s2mod(l,r)", "invalid"],   # Set      
        ["invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "invalid",    "lmod(l,r)"],   # list      
    
        ],
}


# --------------------------------------------------
#        B O O L E A N   O P E R A T I O N S 
# --------------------------------------------------
_evaluate_boolops_fn = {
    TK.AND: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["X",            "X",            "X",            "X",            "X",            "X",            "X",            "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "land(l,r)"],   # list      
    
        ],
    TK.OR: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "l and r",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "lor(l,r)"],   # list      
    
        ],
    TK.ISEQ: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l == r",       "l == r",       "l == r",       "2i:l == r",    "2i:l == r",    "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l == r",       "l == r",       "l == r",       "2f:l == r",    "2f:l == r",    "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l == r",       "l == 2i:r",    "l == 2f:r",    "l == r",       "l == r",       "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l == 2i:r",    "l == 2i:r",    "l == 2f:r",    "l == 2b:r",    "l == r",       "l == 2d:r",    "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "l == r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "siseq(l,r)",   "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2iseq(l,r)",  "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "liseq(l,r)"],   # list      
    
        ],
    TK.NEQ: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l != r",       "l != r",       "l != r",       "2i:l != r",    "2i:l != r",    "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l != r",       "l != r",       "l != r",       "2i:l != r",    "2f:l != r",    "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l != r",       "l != 2i:r",    "l != 2i:r",    "l != r",       "l != r",       "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l != 2i:r",    "l != 2i:r",    "l != 2f:r",    "l != 2b:r",    "l != r",       "l != 2d:r",    "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "l != r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "sneq(l,r)",    "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2neq(l,r)",   "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "lneq(l,r)"],   # list      
    
        ],
    TK.GTR: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l > r",        "l > r",        "l > r",        "2i:l > r",     "2i:l > r",     "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l > r",        "l > r",        "l > r",        "2i:l > r",     "2f:l > r",     "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l > r",        "l > 2i:r",     "l > 2i:r",     "l > r",        "l > r",        "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l > 2i:r",     "l > 2i:r",     "l > 2f:r",     "l > 2b:r",     "l > r",        "l > 2d:r",     "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "l > r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "sgtr(l,r)",    "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2gtr(l,r)",   "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "lgtr(l,r)"],   # list      
    
        ],
    TK.LESS: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l < r",        "l < r",        "l < r",        "2i:l < r",     "2i:l < r",     "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l < r",        "l < r",        "l < r",        "2i:l < r",     "2f:l < r",     "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l < r",        "l < 2i:r",     "l < 2i:r",     "l < r",        "l < r",        "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l < 2i:r",     "l < 2i:r",     "l < 2f:r",     "l < 2b:r",     "l < r",        "l < 2d:r",     "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "l < r",        "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "sless(l,r)",   "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2less(l,r)",  "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "lless(l,r)"],   # list      
    
        ],
    TK.GTE: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l >= r",       "l >= r",       "l >= r",       "2i:l >= r",    "2i:l >= r",    "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l >= r",       "l >= r",       "l >= r",       "2i:l >= r",    "2f:l >= r",    "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l >= r",       "l >= 2i:r",    "l >= 2i:r",    "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l >= 2i:r",    "l >= 2i:r",    "l >= 2f:r",    "l >= 2b:r",    "l >= r",       "l >= 2d:r",    "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "l >= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "sgte(l,r)",    "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2gte(l,r)",   "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "lgte(l,r)"],   # list      
    
        ],
    TK.LTE: [
        #      any            int           float           bool            str         timedelta        Object          Block        DataFrame        Range          Series           Set            list      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # any      
        ["l <= r",       "l <= r",       "l <= r",       "2i:l <= r",    "2i:l <= r",    "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # int      
        ["l <= r",       "l <= r",       "l <= r",       "2i:l <= r",    "2f:l <= r",    "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # float      
        ["l <= r",       "l <= 2i:r",    "l <= 2i:r",    "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # bool      
        ["l <= 2i:r",    "l <= 2i:r",    "l <= 2f:r",    "l <= 2b:r",    "l <= r",       "l <= 2d:r",    "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # str      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # timedelta      
        ["l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "l <= r",       "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Object      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Block      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # DataFrame      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid"],   # Range      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "slte(l,r)",    "invalid",      "invalid"],   # Series      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "s2lte(l,r)",   "invalid"],   # Set      
        ["invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "invalid",      "llte(l,r)"],   # list      
    
        ],
}
