from enum import IntEnum, auto


class TY(IntEnum):
    ENUM = 0
    DICT = auto()
    LIST = auto()


class CodeWriter:

    def __init__(self, logger):
        self.level = 0
        self.linebuf = ""
        self.logger = logger

    def flush(self):
        pass

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

    def print(self, line=None, level=None, append=False, end=None):
        level = self.level if level is None else level
        indent = f'{_get_indent(level)}' if not append else ''
        self.logger.write(f'{indent}{line}', append, end)

    def l_print(self, level, line, end=None):
        self.print(line=line, level=level, end=end)

    def blank_line(self, num=1):
        self.l_print(0, "\n"*num)

    def horiz_line(self, count):
        self.l_print(0, f'# {"-"*count}')

    def banner(self, label):
        self.blank_line(2)
        title = _expand_text(label.upper())
        l = 25 - len(title)//2
        l = 0 if l < 0 else l
        self.l_print(0, f'# {"-"*50}')
        self.l_print(0, f'# {" ".ljust(l)}{title}')
        self.l_print(0, f'# {"-"*50}')

    def sm_banner(self, title):
        self.blank_line(2)
        l = 12 - len(title)//2
        l = 0 if l < 0 else l
        self.l_print(0, f'# {"-"*24}')
        self.l_print(0, f'# {" ".ljust(l)}{title}')
        self.l_print(0, f'# {"-"*24}')

    def define_fn(self, name, params):
        self.l_print(0, f'def {name}({params}):')

    def define_const(self, name, value):
        self.l_print(0, f'{name} = {value}')

    def define_dict(self, name, ty, data=None, quote=True):
        q ='\'' if quote is True else ''
        self.write_open(name, ty)
        if data is not None:
            self.indent()
            idx = 0
            for item in data:
                if ty == TY.ENUM:
                    self.print(f'{q}{item}{q}: {idx},')
                elif ty == TY.LIST:
                    self.print(f'{q}{item}{q}{_get_grouping(ty, GRP.SEP)}')
                elif ty == TY.DICT:
                    val = data[item]
                    v = f'{q}{data[item]}{q}' if isinstance(val, str) else f'{data[item]}'
                    self.print(f'{q}{item}{q}: {v},')
                idx += 1
            self.dedent()
        self.write_close(ty)

    def imports(self, pairs):
        for f in pairs.keys():
            imports = []
            for i in pairs[f]:
                imports.append(f'{i}')
            line = f'from {f} import {", ".join(imports)}'
            self.l_print(0, line)
        self.blank_line(2)

    def write_open(self, name, ty):
        self.print(f'{name} = {_get_grouping(ty, GRP.OPEN)}')

    def write_close(self, ty):
        self.print(f'{_get_grouping(ty, GRP.CLOSE)}')


def _expand_text(text):
    t = []
    for c in text:
        t.append(f'{c} ')
    return ''.join(t)


def _get_indent(level):
    return '' if level < 1 else ' '.ljust(level * 4)


def _get_grouping(ty, grp):
    if ty is not None:
        if ty in _ty2grp:
            return _ty2grp[ty][grp]
    return _DEFAULT_GRP[grp]


# -------------------------------------------------------
#                       D A T A
# -------------------------------------------------------
class GRP(IntEnum):
    OPEN = 0
    SEP = 1
    CLOSE = 2
    EMPTY = 3


_ty2grp = {
    TY.LIST: ['[', ', ', ']', '[]'],
    TY.DICT: ['{', ', ', '}', '{}'],
    TY.ENUM: ['{', ', ', '}', '{}'],
}


_DEFAULT_GRP = ['(', ', ', ')', '()']


