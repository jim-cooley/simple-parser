from numpy import unique, sort

from runtime.token import Token
from runtime.token_data import _tk2binop, _tk2lit, _tk2unop, _tk2type, _tk2glyph, MULTIPLICATION_TOKENS, \
    SET_UNARY_TOKENS, UNARY_TOKENS, IDENTIFIER_TOKENS, EQUALITY_TEST_TOKENS, IDENTIFIER_TOKENS_EX, COMPARISON_TOKENS, \
    LOGIC_TOKENS, ADDITION_TOKENS, VALUE_TOKENS


def get_token_names():
    return [t for t in dir(Token) if t.upper() == t]


# used to build the mapping data.  The constructors below serve to inter the data about all the valid tokens.
def get_tokens():
    return [getattr(Token, f, None)() for f in dir(Token) if f.upper() == f]


def get_token_ids():
    return [getattr(Token, f, None)().id for f in dir(Token) if f.upper() == f]


def get_token_map():
    _m = {}
    tokens = get_tokens()
    for tk in tokens:
        _m[tk.id] = tk
    return _m


def gen_tk2type():
    tokens = get_tokens()
    tk_map = {}
    for tk in tokens:
        tk_map[tk.id] = tk.t_class
    return tk_map


def gen_tk2glyph():
    tokens = get_tokens()
    tk_map = {}
    for tk in tokens:
        tk_map[tk.id] = tk.lexeme
    return tk_map


def gen_token_methods():
    print("\nstatic Token methods:")
    tokens = get_tokens()
    for tk in tokens:
        lex = tk.lexeme or ''
        lex = f"'{lex}'"
        print(f"@staticmethod\n" \
              f"def {tk.id.name.upper()}(loc=None, value=None):\n" \
              f"    return Token(tid=TK.{tk.id.name}, tcl=TCL.{tk.t_class.name}, lex={lex}, val=value, loc=loc)\n" \
              f"\n"
              )


def _pad(width, text, q=False, com=True):
    q = "'" if q else ''
    c = ',' if com else ''
    text = f'{q}{text}{q}{c}'
    return f"{text}{' '.ljust(width-len(text))}"


def _tag(tag, val, q=False, com=True):
    c = ',' if com else ''
    s = ' ' if val else ''
    q = "'" if q else ''
    t = f'{q}{val}{q}{c}{s}'
    return f'{tag}={t}'


def gen_token_data():
    print("\nstatic Token methods:")
    tokens = get_tokens()
    print_token_def()
    print("_token_data = {")
    q = "'"
    for tk in tokens:
        tk_name = f'TK.{tk.id.name}'
        tcl_name = f'TCL.{tk.t_class.name}'
        lex = tk.lexeme or ''
        val = f'{tk.value}'
        line = [
            "   TD( ",
            f"{_tag('tk', tk_name):20s}",
            f"{_tag('tcl',tcl_name):20s}",
            f"{_tag('lex', lex, q=True):14s}",
            f"g='', ",
            f"{_tag('v', val):10s} ",
            f"{_tag('rs', tk.is_reserved):10} ",
            f"{_tag('ml', tk.id in MULTIPLICATION_TOKENS):10}",
            f"{_tag('ad', tk.id in ADDITION_TOKENS):10}",
            f"{_tag('un', tk.id in UNARY_TOKENS):10}",
            f"{_tag('st', tk.id in SET_UNARY_TOKENS):10}",
            f"{_tag('id', tk.id in IDENTIFIER_TOKENS):10}",
            f"{_tag('idx', tk.id in IDENTIFIER_TOKENS_EX):10}",
            f"{_tag('eq', tk.id in EQUALITY_TEST_TOKENS):10}",
            f"{_tag('co', tk.id in COMPARISON_TOKENS):10}",
            f"{_tag('lo', tk.id in LOGIC_TOKENS):10}",
            f"{_tag('isv', tk.id in VALUE_TOKENS, com=False):10}",
        ]

        print(f"{    ''.join(line)}), ")
    print("}")


def print_token_def():
    print("@dataclass\n"
          "class TD:\n"
          "    def __init__(tk=None, tcl=None, lex=None, g=None, v=None, rs=False, ml=False, ad=False, st=False, id=False, eq=False, co=False, lo=False, isv=False):\n"
          "        self.tk = tk\n"
          "        self.tcl = tcl\n"
          "        self.lex = lex\n"
          "        self.glyph = g\n"
          "        self.value = v\n"
          "        self.is_reserved = rs\n"
          "        self.is_multiply = ml\n"
          "        self.is_associative = ad\n"
          "        self.is_unary = un\n"
          "        self.is_identifier = id\n"
          "        self.is_identifier_x = idx\n"
          "        self.is_equality = eq\n"
          "        self.is_comparison = co\n"
          "        self.is_logic = lo\n"
          "        self.is_value = isv\n"
          "\n"
          )


def missing_report():
    tokens = get_tokens()
    tkids = get_token_ids()
    tk_map = get_token_map()
    missing = []
    for tk in tokens:
        if tk.id not in _tk2type:
            missing.append(tk.id.name)
    print('\nmissing from _tk2type:\n')
    print('\n'.join(missing))
    missing = []
    incorrect = []
    for tid in _tk2type:
        if tid not in tkids:
            if tid not in _tk2binop or tid == _tk2binop[tid]:
                if tid not in _tk2unop or tid == _tk2unop[tid]:
                    missing.append(tid.name)
                    if tid in _tk2type and tid in tk_map:
                        if _tk2type[tid] != tk_map[tid]:
                            incorrect.append(tid.name)
    print('\n_tk2type missing from Token that are not mapped: \n')
    print('\n'.join(missing))
    print('\nincorrect type in Token from _tk2type: \n')
    print('\n'.join(incorrect))
    missing = []
    for tk in tokens:
        if tk.id not in _tk2glyph:
            if tid not in _tk2binop or tid == _tk2binop[tid]:
                if tid not in _tk2unop or tid == _tk2unop[tid]:
                    missing.append(tk.id.name)
    print('\nmissing from _tk2glyph that are not mapped:\n')
    print('\n'.join(missing))
    missing = []
    for tid in _tk2glyph:
        if tid not in tkids:
            missing.append(tid.name)
    print('\n_tk2glyph missing from Token: \n')
    print('\n'.join(missing))
    remove = []
    for tid in _tk2binop:
        if tid in tkids and tid != _tk2binop[tid]:  # skip those that map to themselves
            remove.append(tid.name)
    print('\nmapped token ids from _tk2binop that are in Token (should be removed): \n')
    print('\n'.join(remove))
    remove = []
    for tid in _tk2binop:
        if tid != _tk2binop[tid]:  # skip those that map to themselves
            remove.append(tid.name)
    for tid in _tk2unop:
        if tid != _tk2unop[tid]:  # skip those that map to themselves
            remove.append(tid.name)
    print('\nmapped tokens in _tk2binop or _tkunop (should just be mapped in lexer): \n')
    print('\n'.join(unique(sort(remove))))


def _print_dict(name, d, prefix1, prefix2):
    print(f'{name} = '"{")
    for k in d:
        if prefix1 is not None:
            key = f'{prefix1}.{k.name}'
        else:
            key = f'{k}'
        if prefix2 is not None:
            value = f'{prefix2}.{d[k].name}'
        else:
            v = d[k]
            if isinstance(v, str):
                v = f"'{v}'"
            value = f'{v}'
        print(f'    {key}: {value},')
    print("}")


if __name__ == '__main__':
    missing_report()

    tk2type = gen_tk2type()
    print("\n\n")
    _print_dict('_tk2type', tk2type, 'TK', 'TCL')

    tk2glyph = gen_tk2glyph()
    print("\n\n")
    _print_dict('_tk2glyph', tk2glyph, 'TK', None)

    print("\n\n")
    gen_token_methods()

    print("\n\n")
    gen_token_data()
