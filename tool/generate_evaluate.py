#!/Users/jim/venv/jimc/bin/python
import sys
from tokens import TK

from tool.codewriter import LogWriter, CodeWriter, TY
from tool.tables import _assign_obj_fn, _evaluate_boolops_fn, _evaluate_binops_fn


_COLUMNS = ['any', 'int', 'float', 'bool', 'str', 'timedelta', 'Object', 'Block']


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


class GenerateEvalDispatch:
    def __init__(self):
        self.fname = None
        self.file = None
        self._functions = {}
        self.o = None
        self.source = None
        self.is_assign_style = False
        self.width = 18  # function table column width

    def go(self, fname, name, source, width=None, assign_style=False, insert_fixup_dispatch=True, insert_assignment_fixup=False):
        self.fname = fname
        self.source = source
        self.width = self.width if width is None else width
        self.is_assign_style = assign_style
        self.process_dispatch_data(source)
        with open(self.fname, 'w') as file:
            logger = LogWriter(file=file)
            self.o = CodeWriter(logger=logger)
            self.generate_file(name, insert_fixup_dispatch, insert_assignment_fixup)
            self.o.flush()

    # second entry point: reprints the data tables -- be careful.
    def print_tables(self, fname):
        with open(fname, 'w') as file:
            logger = LogWriter(file=file)
            self.o = CodeWriter(logger=logger)
            self.print_table_header()
            self.pretty_print_table('assignment tables', '_assign_obj_fn', _assign_obj_fn, 12, quote=True)
            self.pretty_print_table('binary operations', '_evaluate_binops_fn', _evaluate_binops_fn, 12, quote=True)
            self.pretty_print_table('boolean operations', '_evaluate_boolops_fn', _evaluate_boolops_fn, 14, quote=True)
            self.o.flush()

    def open(self, fname):
        self.fname = fname
        if fname is not None:
            self.file = open(fname, 'w')
        logger = LogWriter(file=self.file)
        self.o = CodeWriter(logger=logger)

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def indent(self):
        self.o.indent()

    def dedent(self):
        self.o.dedent()

    def generate_file(self, name, insert_fixup_dispatch=True, insert_assignment_fixup=False):
        self.write_header(name, insert_fixup_dispatch, insert_assignment_fixup)
        self.write_dispatch_outer(name)
        self.write_dispatch_inner(name)
        self.generate_eval_functions(name)
        self.generate_invalid_op_functions(name)
        self.generate_dispatch_table(name)

    def write_header(self, name, insert_fixup_dispatch=True, insert_assignment_fixup=False):
        self.o.imports({'conversion':['c_box', 'c_to_bool', 'c_to_int', 'c_unbox'],
                        'environment':['Environment'],
                        'exceptions':['runtime_error'],
                        'tokens':['TK'],
                        })
        self.o.horiz_line(98)
        self.o.l_print(0, "# NOTE: This is a generated file.  Please port any manual changes to tool/generate_evaluate.py")
        self.o.horiz_line(98)
        self.o.blank_line(2)
        self.o.define_dict(f'_SUPPORTED_{name.upper()}_OPERATIONS', ty=TY.LIST, data=[f'TK.{_.name}' for _ in self.source.keys()], quote=False)
        self.o.blank_line()
        self.o.define_const('_INTRINSIC_VALUE_TYPES', _COLUMNS)
        self.o.blank_line()
        self.o.define_dict(name='_type2idx', ty=TY.ENUM, data=_COLUMNS)
        self.o.blank_line()
        self.o.define_dict(name='_type2native', ty=TY.DICT, data=_type2native)
        self.o.banner("MANUAL CHANGES")
        if insert_fixup_dispatch:
            self.o.print("# used by fixups\n"
                         f"def eval_{name}_dispatch_fixup(node):\n"
                         "    if node is None:\n"
                         "        return None\n"
                         f"    if node.op in _{name}_dispatch_table:\n"
                         f"        return eval_{name}_dispatch(node, node.left, node.right)\n"
                         "    return node.value")
        if insert_assignment_fixup:
            self.o.print("# referenced in evaluate:\n"
                         "_SUPPORTED_VALUE_TYPES = ['int', 'float', 'bool', 'str', 'timedelta', 'object', 'block']\n"
                         "_SUPPORTED_ASSIGNMENT_TOKENS = [TK.APPLY, TK.ASSIGN, TK.DEFINE]")

    def write_dispatch_outer(self, name):
        self.o.banner("DISPATCH CORE")
        self.o.blank_line(2)
        self.o.define_fn(f'eval_{name}_dispatch', 'node, left, right')
        self.o.l_print(0, "    l_value = left\n"
                          "    if getattr(left, 'value', False):\n"
                          "        l_value = left.value\n"
                          "    l_ty = type(l_value).__name__\n"
                          "    r_value = right\n"
                          "    if getattr(right, 'value', False):\n"
                          "        r_value = right.value\n"
                          "    r_ty = type(r_value).__name__\n"
                          "    if l_ty == 'Ident':\n"
                          "        l_value = Environment.current.scope.find(left.token).value\n"
                          "    if r_ty == 'Ident':\n"
                          "        r_value = Environment.current.scope.find(right.token).value\n"
                          "    if l_value is None or r_value is None:\n"
                          "        return None\n"
                          f"    return eval_{name}_dispatch2(node.token.id, l_value, r_value)")

    def write_dispatch_inner(self, name):
        self.o.blank_line(2)
        self.o.define_fn(f'eval_{name}_dispatch2', 'tkid, l_value, r_value')
        self.o.l_print(0, "    l_ty = type(l_value).__name__\n"
                          "    r_ty = type(r_value).__name__\n"
                          "    l_ty = l_ty if l_ty not in _type2native else _type2native[l_ty]\n"
                          "    r_ty = r_ty if r_ty not in _type2native else _type2native[r_ty]\n"
                          "    if l_ty in _type2idx and r_ty in _type2idx:\n"
                          "        ixl = _type2idx[l_ty]\n"
                          "        ixr = _type2idx[r_ty]\n"
                          f"        fn = _{name}_dispatch_table[tkid][ixr][ixl]\n"
                          "        return fn(l_value, r_value)\n")

    def generate_eval_functions(self, name):
        self.o.banner("OPERATOR FUNCTIONS")
        for code in self._functions.keys():
            fn = self._functions[code]
            if fn[:len('_invalid_')] != '_invalid_':
                self.write_eval_fn(fn, code)

    def write_eval_fn(self, name, code):
        self.o.blank_line(2)
        self.o.define_fn(name.lower(), 'l_value, r_value')
        code = _expand_fragment(code)
        if self.is_assign_style:
            if code[0] is '.':
                self.o.l_print(1, f'l_value{code}')
            else:
                self.o.l_print(1, f'l_value = {code}')
            self.o.l_print(1, 'return l_value')
        else:
            self.o.l_print(1, f'return {code}')

    def generate_invalid_op_functions(self, name):
        self.o.banner("ERROR FUNCTIONS")
        for fn in self.source.keys():
            self.write_invalid_op_fn(fn.name.lower())

    def write_invalid_op_fn(self, name):
        self.o.blank_line(2)
        self.o.define_fn(f'_invalid_{name.lower()}', 'left, right')
        self.o.l_print(1, f'runtime_error(f\'Type mismatch for operator {name}('
                       '{type(left)}, {type(right)})\', loc=None)')

    def generate_dispatch_table(self, name):
        self.o.banner("DISPATCH TABLE")
        self.o.write_open(f"_{name}_dispatch_table", TY.DICT)
        for op in self.source:
            self.generate_operation_dispatch_fragment(op)
        self.o.write_close(TY.DICT)

    # -------------------------------

    def generate_operation_dispatch_fragment(self, op):
        sep = ', '
        width = self.width
        self.indent()
        table = self.source[op]
        self.o.print(f'TK.{op.name}: [')
        self.indent()
        self.o.l_print(2, '#', end='')
        for c in _COLUMNS:
            self.o.print(f'{c:^{width}s}', end='', append=True)
        self.o.blank_line(1)
        for r in range(0, len(table)):
            self.o.print('[', end='')
            _len = len(table[r])
            for c in range(0, _len):
                code = table[r][c]
                if code == 'invalid':
                    fn = f'_invalid_{op.name.lower()}'
                    self.o.print(f'{fn}', end='', append=True)
                else:
                    fn = self._functions[code].lower()
                    self.o.print(f'{fn}', end='', append=True)
                if c < _len - 1:
                    pad = max(width-len(fn), 0)
                    self.o.print(f'{sep:{pad}s}', end='', append=True)
            self.o.print('],   # ', end='', append=True)
            self.o.print(f'{_COLUMNS[r]}      ', append=True)
        self.dedent()
        self.o.print('\n    ],')
        self.dedent()

    def process_dispatch_data(self, source):
        self._functions = {}
        for op in source.keys():
            table = source[op]
            for r in range(0, len(table)):
                for c in range(0, len(table[r])):
                    code = table[r][c]
                    if code in self._functions:
                        continue
                    fn = f'_{op.name.lower()}__{_COLUMNS[c]}_{_COLUMNS[r]}' if code != 'invalid' else f'_invalid_{op.name.lower()}'
                    self._functions[code] = fn

    # -------------------------------

    def print_table_header(self):
        self.o.print("from tokens import TK")
        self.o.banner("TABLES")
        self.o.print("# 'any' is used to denote the generic routine instead of everything ending up appearing as an int_ conversion\n"
                     "\n"
                     "# abbreviations in table:\n"
                     "#   l = l_value     2i = c_to_int    2f = c_to_float    u = unbox       s( ) = f'{ }'\n"
                     "#   r = r_value     2b = c_to_bool   2d = c_to_dur      b = box         .o( ) = .from_object( )\n"
                     "#                                                                       .b( ) = .from_block( )\n"
                     "#                                                                       v( ) = .value =\n"
                     "#\n"
                     "#   B = TK.BOOL     D = TK.DUR       F = TK.FLOT        I = TK.INT      L = TK.LIST     O = TK.OBJECT   S = TK.STR\n")

    def pretty_print_table(self, name, identifier, table, width, quote=False):
        self.o.banner(f"{name.upper()}")
        self.o.write_open(f"{identifier}", TY.DICT)
        for op in table:
            self._pretty_print_table_section(table=table[op], sect=op, width=width, quote=quote)
        self.o.write_close(TY.DICT)

    def _pretty_print_table_section(self, table, sect, width, quote=False):
        q = '\"' if quote is True else ''
        sep = ', '
        self.indent()
        self.o.print(f'TK.{sect.name}: [')
        self.indent()
        self.o.l_print(2, '#', end='')
        for c in _COLUMNS:
            self.o.print(f'{c:^{width}s}', end='', append=True)
        self.o.blank_line(1)
        for r in range(0, len(table)):
            self.o.print('[', end='')
            _len = len(table[r])
            for c in range(0, _len):
                code = table[r][c]
                self.o.print(f'{q}{code}{q}', end='', append=True)
                if c < _len - 1:
                    pad = max(width-len(code), 0)
                    self.o.print(f'{sep:{pad}s}', end='', append=True)
            self.o.print('],   # ', end='', append=True)
            self.o.print(f'{_COLUMNS[r]}      ', append=True)
        self.dedent()
        self.o.print('\n    ],')
        self.dedent()


def _expand_fragment(code):
    code = "r_value" if code == "r" else code
    code = code.replace("l ", "l_value ").replace(" r", " r_value") \
        .replace("{r", "{r_value").replace("{l", "{l_value") \
        .replace("(r", "(r_value").replace("(l", "(l_value") \
        .replace(" B)", " TK.BOOL)").replace(" I)", " TK.INT)") \
        .replace(" D)", " TK.DUR)").replace(" F)", " TK.FLOT)") \
        .replace(" L)", " TK.LIST)").replace(" O)", " TK.OBJECT)").replace(" S)", " TK.STR)") \
        .replace("2i(", "c_to_int(").replace("2b(", "c_to_bool(") \
        .replace("2f(", "c_to_float(").replace("2d(", "c_to_dur(") \
        .replace(".b(r_value)", ".from_block(r_value)").replace("u(", "c_unbox(").replace("b(", "c_box(") \
        .replace("s(l_value)", "f'{l_value}'").replace("s(r_value)", "f'{r_value}'").replace(".v(r_value)", ".value = r_value") \
        .replace(".o(r_value)", ".from_object(r_value)")
    return code


# -------------------------------------------------------
#                       M A I N
# -------------------------------------------------------
def main(args):
    gen = GenerateEvalDispatch()
    gen.go('eval_binops.py', 'binops', _evaluate_binops_fn)
    gen.go('eval_boolean.py', 'boolean', _evaluate_boolops_fn, insert_fixup_dispatch=False)
    gen.go('eval_assignment.py', 'assign', _assign_obj_fn,
           assign_style=True, insert_fixup_dispatch=False, insert_assignment_fixup=True, width=24)

    gen = GenerateEvalDispatch()
    gen.print_tables('tables.py')


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)

