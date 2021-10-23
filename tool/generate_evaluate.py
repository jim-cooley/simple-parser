#!/Users/jim/venv/jimc/bin/python
import sys
from tokens import TK

_COLUMNS = ['int', 'float', 'bool', 'str']

_evaluate_binops_fn = {
    TK.ADD: [
        #     int         float           bool             str
        ['l + r',       'l + r',        'l + r',        "l + f'{r}'"],    # int
        ['l + r',       'l + r',        'l + r',        "l + f'{r}'"],    # float
        ['l + r',       'l + r',        'l + r',        "l + f'{r}'"],    # bool
        ["f'{l}' + r",  "f'{l}' + r",   "f'{l}' + r",   "l + r"],         # str
    ],
    TK.SUB: [
        #     int         float           bool             str
        ['l - r',       'l - r',        'l - r',        "invalid"],       # int
        ['l - r',       'l - r',        'l - r',        "invalid"],       # float
        ['l - r',       'l - r',        'l - r',        "invalid"],       # bool
        ['invalid',     "invalid",      "invalid",      "invalid"],       # str
    ],
    TK.DIV: [
        #     int         float           bool             str
        ['l / r',       'l / r',        'l / r',        "invalid"],       # int
        ['l / r',       'l / r',        'l / r',        "invalid"],       # float
        ['l / r',       'l / r',        'l / r',        "invalid"],       # bool
        ['invalid',     "invalid",      "invalid",      "invalid"],       # str
    ],
    TK.POW: [
        #     int         float           bool             str
        ['l ** r',       'l ** r',        'l ** r',        "invalid"],       # int
        ['l ** r',       'l ** r',        'l ** r',        "invalid"],       # float
        ['l ** r',       'l ** r',        'l ** r',        "invalid"],       # bool
        ['invalid',     "invalid",      "invalid",      "invalid"],       # str
    ],
    TK.MUL: [
        #     int         float           bool             str
        ['l * r',       'l * r',        'l * r',        "l * r"],       # int
        ['l * r',       'l * r',        'l * r',        "l * r"],       # float
        ['l * r',       'l * r',        'l * r',        "l * r"],       # bool
        ['l * r',       "l * r",        "l * r",        "l * r"],       # str
    ]
}

_functions = {}


def main(args):
    fname = args[0]
    process_dispatch_data()
    print(_functions)
    with open(fname, 'w') as file:
        _write_preamble(file)
        generate_dispatch_function(file, 'binops')
        generate_eval_functions(file)
        generate_invalid_op_functions(file)
        generate_dispatch_table(file, 'binops')


def generate_dispatch_function(f, name):
    _write_define_fn(f, name, 'node')
    _t_print(f, 1, f"if node.token.id in _{name}_dispatch_table:")
    _t_print(f, 2, "left = node.left")
    _t_print(f, 2, "l_ty = type(left.value).__name__")
    _t_print(f, 2, "right = node.right")
    _t_print(f, 2, "r_ty = type(right.value).__name__")
    _t_print(f, 2, "if l_ty in _type2idx and r_ty in _type2idx:")
    _t_print(f, 3, "ixl = _type2idx[l_ty]")
    _t_print(f, 3, "ixr = _type2idx[r_ty]")
    _t_print(f, 3, f'fn = _{name}_dispatch_table[node.token.id][ixr][ixl]')
    _t_print(f, 3, 'return fn(left, right)')
    _t_print(f, 1, "_error(f'Invalid operation {node.token.id.name}', loc=node.token.location)")
    _t_print(f, 0, "\n")


def generate_eval_functions(f):
    for code in _functions.keys():
        fn = _functions[code]
        if fn[:len('_invalid_')] != '_invalid_':
            generate_eval_fn(f, fn, code)


def generate_eval_fn(f, name, code):
    _write_binop_fn_preamble(f, name)
    _t_print(f, 1, f'return {code}\n')


def generate_invalid_op_functions(f):
    for fn in _evaluate_binops_fn.keys():
        generate_invalid_op_fn(f, fn.name.lower())


def generate_invalid_op_fn(f, name):
    _write_define_fn(f, f'_invalid_{name}', 'left, right')
    _t_print(f, 1, f'_runtime_error(f\'Type mismatch for operator {name}('
                   '{type(left)}, {type(right)})\', loc=None)\n')


def generate_operation_dispatch_fragment(f, op):
    tab = 1
    table = _evaluate_binops_fn[op]
    _t_print(f, tab, f'TK.{op.name}: [')
    tab += 1
    _t_print(f, tab,  '#      ', end='')
    for c in _COLUMNS:
        _t_print(f, 0, f'{c}           ', end='')
    _t_print(f, 0, '')
    for r in range(0, len(table)):
        _t_print(f, tab, '[', end='')
        _len = len(table[r])
        for c in range(0, _len):
            code = table[r][c]
            if code == 'invalid':
                _t_print(f, 0, f'_invalid_{op.name.lower()}', end='')
            else:
                _t_print(f, 0, _functions[code], end='')
            if c < _len - 1:
                _t_print(f, 0, ', ', end='')
        _t_print(f, 0, '],   # ', end='')
        _t_print(f, 0, f'{_COLUMNS[r]}      ')
    tab = 1
    _t_print(f, tab, '\n    ],')


def process_dispatch_data():
    for op in _evaluate_binops_fn.keys():
        table = _evaluate_binops_fn[op]
        for r in range(0, len(table)):
            for c in range(0, len(table[r])):
                code = table[r][c]
                if code in _functions:
                    continue
                fn = f'_{op.name.lower()}__{_COLUMNS[c]}_{_COLUMNS[r]}' if code != 'invalid' else f'_invalid_{op.name.lower()}'
                _functions[code] = fn


def generate_dispatch_table(file, name):
    _t_print(file, 0, f"_{name}_dispatch_table = ""{\n")
    for op in _evaluate_binops_fn:
        generate_operation_dispatch_fragment(file, op)
    _t_print(file, 0, "}\n\n")


def _write_binop_fn_preamble(f, name):
    _write_define_fn(f, name, 'left, right')
    _t_print(f, 1,  "l = left.value")
    _t_print(f, 1,  "r = right.value")


def _write_define_fn(f, name, params):
    _t_print(f, 0, f'def {name}({params}):')


def _write_preamble(file):
    _t_print(file, 0, "from exceptions import _runtime_error, _error\n"
                      "from tokens import TK\n"
                      "\n"
                      "_INTRINSIC_VALUE_TYPES = ['int', 'float', 'bool', 'str']\n"
                      "\n"
                      "\n"
                      "_type2idx = {\n"
                      "    'int': 1,\n"
                      "    'float': 2,\n"
                      "    'bool': 3,\n"
                      "    'str': 4,\n"
                      "}\n\n")


def _get_indent(level):
    return '' if level < 1 else ' '.ljust(level * 4)


def _t_print(f, level, message, end='\n'):
    end = '' if end is None else end
    indent = _get_indent(level)
    print(f'{indent}{message}', end=end)
    if f is not None:
        f.write(f'{indent}{message}{end}')


# this is only for execution under debugger or via command-line
if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)