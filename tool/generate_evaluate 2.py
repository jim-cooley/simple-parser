#!/Users/jim/venv/jimc/bin/python
import sys
from tool.codewriter import LogWriter, CodeWriter, TY
from tokens import TK


# -------------------------------------------------------
#                       T A B L E
# -------------------------------------------------------
# 'any' is used to denote the generic routine instead of everything ending up appearing as an int_ conversion

_COLUMNS = ['any', 'int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block']

# abbreviations in table:
#   l = l_value     2i = c_to_int    2f = c_to_float    u = unbox       s( ) = f'{ }'
#   r = r_value     2b = c_to_bool   2d = c_to_dur      b = box
#
#   B = TK.BOOL     D = TK.DUR       F = TK.FLOT        I = TK.INT      L = TK.LIST     O = TK.OBJECT   S = TK.STR


_evaluate_binops_fn = {
    TK.ADD: [
        #   any          int          float           bool               str            dur       object      block
        ['l + r',     'l + r',       'l + r',        'l + r',        "l + s(r)",    'l + r',    'l + r',   "invalid"],    # any
        ['l + r',     'l + r',       'l + r',        'l + r',        "l + s(r)",    'l + r',    'u(l) + r',"invalid"],    # int
        ['l + r',     'l + r',       'l + r',        'l + r',        "l + s(r)",    'l + r',    'l + r',   "invalid"],    # float
        ['l + r',     'l + r',       'l + r',        'l + r',        "l + s(r)",    'l + r',    'l + r',   "invalid"],    # bool
        ["f'{l}' + r", "s(l) + r",   "s(l) + r",     "s(l) + r",      "invalid",    'invalid',  'invalid', "invalid"],    # str
        ['l + r',     'l + r',       'l + r',        'l + r',        "l + s(r)",    'l + r',    'l + r',   "invalid"],    # dur
        ['l + r',     'l + u(r)',    'l + r',        'l + r',        "l + s(r)",    'l + r',    'l + r',   "invalid"],    # object
        ['invalid',   'invalid',     'invalid',      'invalid',      "invalid",     'invalid',  'invalid', "invalid"],    # block
    ],
    TK.SUB: [
        #   any          int          float           bool               str             dur       object     block
        ['l - r',     'l - r',       'l - r',        'l - r',        "invalid",      'l - r',    'l - r',   "invalid"],    # any
        ['l - r',     'l - r',       'l - r',        'l - r',        "invalid",      'l - r',    'u(l) - r',"invalid"],    # int
        ['l - r',     'l - r',       'l - r',        'l - r',        "invalid",      'l - r',    'l - r',   "invalid"],    # float
        ['l - r',     'l - r',       'l - r',        'l - r',        "invalid",      'l - r',    'l - r',   "invalid"],    # bool
        ['invalid',   'invalid',     "invalid",      "invalid",      "invalid",      'l - r',    'l - r',   "invalid"],    # str
        ['l - r',     'l - r',       'l - r',        'l - r',        "invalid",      'l - r',    'l - r',   "invalid"],    # dur
        ['l - r',     'l - u(r)',    'l - r',        'l - r',        "invalid",      'l - r',    'l - r',   "invalid"],    # object
        ['invalid',   'invalid',     'invalid',      'invalid',      "invalid",      'invalid',  'invalid', "invalid"],    # block
    ],
    TK.DIV: [
        #   any          int          float           bool               str             dur       object     block
        ['l / r',     'l / r',       'l / r',        'l / r',        "invalid",      'l / r',    'l / r',    "invalid"],    # any
        ['l / r',     'l / r',       'l / r',        'l / r',        "invalid",      'l / r',    'u(l) / r', "invalid"],    # int
        ['l / r',     'l / r',       'l / r',        'l / r',        "invalid",      'l / r',    'l / r',    "invalid"],    # float
        ['l / r',     'l / r',       'l / r',        'l / r',        "invalid",      'l / r',    'l / r',    "invalid"],    # bool
        ['invalid',   'invalid',     "invalid",      "invalid",      "invalid",      'l / r',    'l / r',    "invalid"],    # str
        ['l / r',     'l / r',       'l / r',        'l / r',        "invalid",      'l / r',    'l / r',    "invalid"],    # dur
        ['l / r',     'l / u(r)',    'l / r',        'l / r',        "invalid",      'l / r',    'l / r',    "invalid"],    # object
        ['invalid',   'invalid',     'invalid',      'invalid',      "invalid",      'invalid',  'invalid',  "invalid"],    # block
    ],
    TK.IDIV: [
        #     any          int       float           bool               str             dur       object        block
        ['l // r',    'l // r',       'l // r',        'l // r',     "invalid",      'l // r',   'l // r',   "invalid"],    # any
        ['l // r',    'l // r',       'l // r',        'l // r',     "invalid",      'l // r',   'u(l) // r', "invalid"],    # int
        ['l // r',    'l // r',       'l // r',        'l // r',     "invalid",      'l // r',   'l // r',   "invalid"],    # float
        ['l // r',    'l // r',       'l // r',        'l // r',     "invalid",      'l // r',   'l // r',   "invalid"],    # bool
        ['invalid',   'invalid',      "invalid",       "invalid",    "invalid",      'l // r',   'l // r',   "invalid"],    # str
        ['l // r',    'l // r',       'l // r',        'l // r',     "invalid",      'l // r',   'l // r',   "invalid"],    # dur
        ['l // r',    'l // u(r)',    'l // r',        'l // r',     "invalid",      'l // r',   'l // r',   "invalid"],    # object
        ['invalid',   'invalid',      'invalid',       'invalid',    "invalid",      'invalid',  'invalid',  "invalid"],    # block
    ],
    TK.POW: [
        #     any          int       float           bool               str             dur       object        block
        ['l ** r',    'l ** r',       'l ** r',        'l ** r',     "invalid",      'l ** r',   'l ** r',   "invalid"],    # any
        ['l ** r',    'l ** r',       'l ** r',        'l ** r',     "invalid",      'l ** r',   'u(l) ** r', "invalid"],    # int
        ['l ** r',    'l ** r',       'l ** r',        'l ** r',     "invalid",      'l ** r',   'l ** r',   "invalid"],    # float
        ['l ** r',    'l ** r',       'l ** r',        'l ** r',     "invalid",      'l ** r',   'l ** r',   "invalid"],    # bool
        ['invalid',   'invalid',      "invalid",       "invalid",    "invalid",      'l ** r',   'l ** r',   "invalid"],    # str
        ['l ** r',    'l ** r',       'l ** r',        'l ** r',     "invalid",      'l ** r',   'l ** r',   "invalid"],    # dur
        ['l ** r',    'l ** u(r)',    'l ** r',        'l ** r',     "invalid",      'l ** r',   'l ** r',   "invalid"],    # object
        ['invalid',   'invalid',      'invalid',       'invalid',    "invalid",      'invalid',  'invalid', "invalid"],    # block
    ],
    TK.MUL: [
        #   any          int       float           bool               str             dur       object        block
        ['l * r',     'l * r',       'l * r',        'l * r',        "l * r",        "l * r",    "l * r",    "invalid"],     # any
        ['l * r',     'l * r',       'l * r',        'l * r',        "l * r",        "l * r",    "u(l) * r", "invalid"],     # int
        ['l * r',     'l * r',       'l * r',        'l * r',        "l * r",        "l * r",    "l * r",    "invalid"],     # float
        ['l * r',     'l * r',       'l * r',        'l * r',        "invalid",      "l * r",    "l * r",    "invalid"],     # bool
        ['l * r',     'l * r',       "l * r",        "l * r",        "invalid",      "l * r",    "l * r",    "invalid"],     # str
        ['l * r',     'l * r',       'l * r',        'l * r',        "invalid",      "l * r",    "l * r",    "invalid"],     # dur
        ['l * r',     'l * u(r)',    'l * r',        'l * r',        "invalid",      "l * r",    "l * r",    "invalid"],     # object
        ['invalid',   'invalid',     'invalid',      'invalid',      "invalid",      'invalid',  'invalid',  "invalid"],    # block
    ],
    TK.MOD: [
        #   any          int         float           bool               str             dur       object        block
        ['l % r',     'l % r',      'l % r',        'l % r',         "l % r",        "l % r",    "l % r",    "invalid"],     # any
        ['l % r',     'l % r',      'l % r',        'l % r',         "l % r",        "l % r",    "u(l) % r", "invalid"],     # int
        ['l % r',     'l % r',      'l % r',        'l % r',         "l % r",        "l % r",    "l % r",    "invalid"],     # float
        ['l % r',     'l % r',      'l % r',        'l % r',         "l % r",        "l % r",    "l % r",    "invalid"],     # bool
        ['l % r',     'l % r',      "l % r",        "l % r",         "l % r",        "l % r",    "l % r",    "invalid"],     # str
        ['l % r',     'l % r',      'l % r',        'l % r',         "l % r",        "l % r",    "l % r",    "invalid"],     # dur
        ['l % r',     'l % u(r)',   'l % r',        'l % r',         "l % r",        "l % r",    "l % r",    "invalid"],     # object
        ['invalid',   'invalid',     'invalid',      'invalid',      "invalid",      'invalid',  'invalid', "invalid"],    # block
    ],
    TK.AND: [
        #     int       float           bool               str             dur       object        block
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # int
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # float
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # bool
        ['l and r', 'l and r',   "l and r",      "l and r",        "l and r",      "l and r",  "l and r",    "invalid"],   # str
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # dur
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # object
        ['invalid', 'invalid',     'invalid',      'invalid',      "invalid",      'invalid',  'invalid', "invalid"],    # block
    ],
    TK.OR: [
        #    any        int       float             bool              str             dur       object        block
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # any
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # int
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # float
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # bool
        ['l and r', 'l and r',   "l and r",      "l and r",        "l and r",      "l and r",  "l and r",    "invalid"],   # str
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # dur
        ['l and r', 'l and r',   'l and r',      'l and r',        "l and r",      "l and r",  "l and r",    "invalid"],   # object
        ['invalid', 'invalid',   'invalid',      'invalid',        "invalid",      'invalid',  'invalid',    "invalid"],   # block
    ],
    TK.ISEQ: [
        #    any        int       float          bool              str            dur       object        block
        ['l == r',  'l == r',   'l == r',      'l == r',        "l == r",      "l == r",  "l == r",    "invalid"],   # any
        ['l == r',  'l == r',   'l == r',      'l == 2b(r, I)', "l == r",      "l == r",  "l == r",    "invalid"],   # int
        ['l == r',  'l == r',   'l == r',      'l == r',        "l == r",      "l == r",  "l == r",    "invalid"],   # float
        ['l == r',  'l == 2i(r, B)',
                                'l == r',      'l == r',        "l == r",      "l == r",  "l == r",    "invalid"],   # bool
        ['l == r',  'l == r',   "l == r",      "l == r",        "l == r",      "l == r",  "l == r",    "invalid"],   # str
        ['l == r',  'l == r',   'l == r',      'l == r',        "l == r",      "l == r",  "l == r",    "invalid"],   # dur
        ['l == r',  'l == r',   'l == r',      'l == r',        "l == r",      "l == r",  "l == r",    "invalid"],   # object
        ['invalid', 'invalid',  'invalid',     'invalid',       "invalid",     'invalid', 'invalid',   "invalid"],   # block
    ],
    TK.NEQ: [
        #    any        int       float          bool              str            dur       object        block
        ['l != r',  'l != r',   'l != r',      'l != r',        "l != r",      "l != r",  "l != r",    "invalid"],   # any
        ['l != r',  'l != r',   'l != r',      'l != 2b(r, I)', "l != r",      "l != r",  "l != r",    "invalid"],   # int
        ['l != r',  'l != r',   'l != r',      'l != r',        "l != r",      "l != r",  "l != r",    "invalid"],   # float
        ['l != r',  'l != 2i(r, B)',
                                'l != r',      'l != r',        "l != r",      "l != r",  "l != r",    "invalid"],   # bool
        ['l != r',  'l != r',   "l != r",      "l != r",        "l != r",      "l != r",  "l != r",    "invalid"],   # str
        ['l != r',  'l != r',   'l != r',      'l != r',        "l != r",      "l != r",  "l != r",    "invalid"],   # dur
        ['l != r',  'l != r',   'l != r',      'l != r',        "l != r",      "l != r",  "l != r",    "invalid"],   # object
        ['invalid', 'invalid',  'invalid',     'invalid',       "invalid",     'invalid', 'invalid',   "invalid"],   # block
    ],
    TK.GTR: [
        #  any        int        float        bool             str            dur     object       block
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # any
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # int
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # float
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # bool
        ['l > r',   'l > r',   "l > r",      "l > r",        "l > r",      "l > r",  "l > r",    "invalid"],   # str
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # dur
        ['l > r',   'l > r',   'l > r',      'l > r',        "l > r",      "l > r",  "l > r",    "invalid"],   # object
        ['invalid', 'invalid', 'invalid',    'invalid',      "invalid",    'invalid','invalid',  "invalid"],   # block
    ],
    TK.LESS: [
        #  any        int        float        bool             str            dur     object       block
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # any
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # int
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # float
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # bool
        ['l < r',   'l < r',   "l < r",      "l < r",        "l < r",      "l < r",  "l < r",    "invalid"],   # str
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # dur
        ['l < r',   'l < r',   'l < r',      'l < r',        "l < r",      "l < r",  "l < r",    "invalid"],   # object
        ['invalid', 'invalid', 'invalid',    'invalid',      "invalid",    'invalid','invalid',  "invalid"],   # block
    ],
    TK.GTE: [
        #  any        int         float          bool             str            dur       object       block
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # any
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # int
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # float
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # bool
        ['l >= r',  'l >= r',   "l >= r",      "l >= r",        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # str
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # dur
        ['l >= r',  'l >= r',   'l >= r',      'l >= r',        "l >= r",      "l >= r",  "l >= r",    "invalid"],   # object
        ['invalid', 'invalid',  'invalid',     'invalid',       "invalid",     'invalid', 'invalid',   "invalid"],   # block
    ],
    TK.LTE: [
        #  any        int         float          bool             str            dur       object       block
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # any
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # int
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # float
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # bool
        ['l <= r',  'l <= r',   "l <= r",      "l <= r",        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # str
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # dur
        ['l <= r',  'l <= r',   'l <= r',      'l <= r',        "l <= r",      "l <= r",  "l <= r",    "invalid"],   # object
        ['invalid', 'invalid',  'invalid',     'invalid',       "invalid",     'invalid', 'invalid',   "invalid"],   # block
    ],
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


_functions = {}


class GenerateEvalDispatch:
    def __init__(self, fname):
        self.fname = fname
        self._functions = {}
        self.o = None

    def go(self, name):
        self.process_dispatch_data()
        with open(self.fname, 'w') as file:
            logger = LogWriter(file=file)
            self.o = CodeWriter(logger=logger)
            self.generate_file(name)
            self.o.flush()

    def indent(self):
        self.o.indent()

    def dedent(self):
        self.o.dedent()

    def generate_file(self, name):
        self.write_header(name)
        self.write_dispatch_outer(name)
        self.write_dispatch_inner(name)
        self.generate_eval_functions(name)
        self.generate_invalid_op_functions(name)
        self.generate_dispatch_table(name)

    def write_header(self, name):
        self.o.imports({'conversion':['c_box', 'c_to_bool', 'c_to_int', 'c_unbox'],
                        'environment':['Environment'],
                        'exceptions':['runtime_error'],
                        'tokens':['TK'],
                        })
        self.o.horiz_line(98)
        self.o.l_print(0, "# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py")
        self.o.horiz_line(98)
        self.o.blank_line(2)
        self.o.define_const('_INTRINSIC_VALUE_TYPES', _COLUMNS)
        self.o.blank_line()
        self.o.define_dict(name='_type2idx', ty=TY.ENUM, data=_COLUMNS)
        self.o.blank_line()
        self.o.define_dict(name='_type2native', ty=TY.DICT, data=_type2native)
        self.o.banner("MANUAL CHANGES")
        self.o.print("# used by fixups\n"
                     "def eval_binops_dispatch_fixup(node):\n"
                     "    if node is None:\n"
                     "        return None\n"
                     "    if node.op in _binops_dispatch_table:\n"
                     "        return eval_binops_dispatch(node, node.left, node.right)\n"
                     "    return node.value")

    def write_dispatch_outer(self, name):
        self.o.banner("DISPATCH CORE")
        self.o.blank_line(2)
        self.o.define_fn(f'eval_{name}_dispatch', 'node, left, right')
        self.o.l_print(1, "l_value = left")
        self.o.l_print(1, "if getattr(left, 'value', False):")
        self.o.l_print(2,   "l_value = left.value")
        self.o.l_print(1, "l_ty = type(l_value).__name__")
        self.o.l_print(1, "r_value = right")
        self.o.l_print(1, "if getattr(right, 'value', False):")
        self.o.l_print(2,   "r_value = right.value")
        self.o.l_print(1, "r_ty = type(r_value).__name__")
        self.o.l_print(1, "if l_ty == 'Ident':")
        self.o.l_print(2,   "l_value = Environment.current.scope.find(left.token).value")
        self.o.l_print(1, "if r_ty == 'Ident':")
        self.o.l_print(2,   "r_value = Environment.current.scope.find(right.token).value")
        self.o.l_print(1, "if l_value is None or r_value is None:")
        self.o.l_print(2,   "return None")
        self.o.l_print(1, "return eval_binops_dispatch2(node.token.id, l_value, r_value)")

    def write_dispatch_inner(self, name):
        self.o.blank_line(2)
        self.o.define_fn(f'eval_{name}_dispatch2', 'tkid, l_value, r_value')
        self.o.l_print(1, "l_ty = type(l_value).__name__")
        self.o.l_print(1, "r_ty = type(r_value).__name__")
        self.o.l_print(1, "l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]")
        self.o.l_print(1, "r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]")
        self.o.l_print(1, "if l_ty in _type2idx and r_ty in _type2idx:")
        self.o.l_print(2,   "ixl = _type2idx[l_ty]")
        self.o.l_print(2,   "ixr = _type2idx[r_ty]")
        self.o.l_print(2,   "fn = _binops_dispatch_table[tkid][ixr][ixl]")
        self.o.l_print(2,   "return fn(l_value, r_value)")

    def generate_eval_functions(self, name):
        self.o.banner("OPERATOR FUNCTIONS")
        for code in self._functions.keys():
            fn = self._functions[code]
            if fn[:len('_invalid_')] != '_invalid_':
                self.write_eval_fn(fn, code)

    def write_eval_fn(self, name, code):
        self.o.blank_line(2)
        self.o.define_fn(name.lower(), 'l_value, r_value')
        code = code.replace("l ", "l_value ").replace(" r", " r_value")\
            .replace("{r", "{r_value").replace("{l", "{l_value")\
            .replace("(r", "(r_value").replace("(l", "(l_value") \
            .replace(" B)", " TK.BOOL)").replace(" I)", " TK.INT)")\
            .replace(" D)", " TK.DUR)").replace(" F)", " TK.FLOT)") \
            .replace(" L)", " TK.LIST)").replace(" O)", " TK.OBJECT)").replace(" S)", " TK.STR)")\
            .replace("2i(", "c_to_int(").replace("2b(", "c_to_bool(") \
            .replace("2f(", "c_to_float(").replace("2d(", "c_to_dur(") \
            .replace("u(", "c_unbox(").replace("b(", "c_box(")\
            .replace("s(l_value)", "f'{l_value}'").replace("s(r_value)", "f'{r_value}'")
        self.o.l_print(1, f'return {code}')

    def generate_invalid_op_functions(self, name):
        self.o.banner("ERROR FUNCTIONS")
        for fn in _evaluate_binops_fn.keys():
            self.write_invalid_op_fn(fn.name.lower())

    def write_invalid_op_fn(self, name):
        self.o.blank_line(2)
        self.o.define_fn(f'_invalid_{name.lower()}', 'left, right')
        self.o.l_print(1, f'runtime_error(f\'Type mismatch for operator {name}('
                       '{type(left)}, {type(right)})\', loc=None)')

    def generate_dispatch_table(self, name):
        self.o.banner("DISPATCH TABLE")
        self.o.write_open(f"_{name}_dispatch_table", TY.DICT)
        for op in _evaluate_binops_fn:
            self.generate_operation_dispatch_fragment(op)
        self.o.write_close(TY.DICT)

    # -------------------------------

    def generate_operation_dispatch_fragment(self, op):
        self.indent()
        table = _evaluate_binops_fn[op]
        self.o.print(f'TK.{op.name}: [')
        self.indent()
        self.o.l_print(2, '#      ', end='')
        for c in _COLUMNS:
            self.o.print(f'{c}       ', end='', append=True)
        self.o.blank_line(1)
        for r in range(0, len(table)):
            self.o.print('[', end='')
            _len = len(table[r])
            for c in range(0, _len):
                code = table[r][c]
                if code == 'invalid':
                    self.o.print(f'_invalid_{op.name.lower()}', end='', append=True)
                else:
                    self.o.print(f'{self._functions[code].lower()}', end='', append=True)
                if c < _len - 1:
                    self.o.print(', ', end='', append=True)
            self.o.print('],   # ', end='', append=True)
            self.o.print(f'{_COLUMNS[r]}      ', append=True)
        self.dedent()
        self.o.print('\n    ],')
        self.dedent()

    def process_dispatch_data(self):
        for op in _evaluate_binops_fn.keys():
            table = _evaluate_binops_fn[op]
            for r in range(0, len(table)):
                for c in range(0, len(table[r])):
                    code = table[r][c]
                    if code in self._functions:
                        continue
                    fn = f'_{op.name.lower()}__{_COLUMNS[c]}_{_COLUMNS[r]}' if code != 'invalid' else f'_invalid_{op.name.lower()}'
                    self._functions[code] = fn


# -------------------------------------------------------
#                       M A I N
# -------------------------------------------------------
def main(args):
    gen = GenerateEvalDispatch(args[0])
    gen.go('binops')


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)

