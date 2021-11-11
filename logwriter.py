

class LogWriter:
    def __init__(self, file=None, auto_flush=True):
        self.file = file
        self.linebuf = []
        self.auto_flush = auto_flush

    def close(self):
        if self.file is not None:
            self.file.flush()
            self.file.close()
            self.file = None

    def open(self, fname):
        self.file = open(fname, 'w')

    def write(self, buf, append=False, end=None):
        end = '\n' if end is None else end
        for line in buf.splitlines():
            print(f'{line}', end=end)
            if not append:
                self.linebuf.append(line)
            else:
                self.linebuf[len(self.linebuf) - 1] += line
            if self.file is not None:
                self.file.write(f'{line}{end}')
                if self.auto_flush:
                    self.file.flush()

    def format(self):
        return '\n'.join(self.linebuf)

    def flush(self):
        if self.file is not None:
            self.file.flush()


class IndentedLogWriter(LogWriter):

    def __init__(self, file=None):
        super().__init__(file=file)
        self.level = 0

    def flush(self):
        super().flush()

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

    def print(self, message=None, level=None, append=False, end=None):
        level = self.level if level is None else level
        indent = f'{_get_indent(level)}' if not append else ''
        self.write(f'{indent}{message}', append, end)

    def l_print(self, level, message, end=None):
        self.print(message=message, level=level, end=end)

    def blank_line(self, num=1):
        self.l_print(0, "\n"*num)

    def horiz_line(self, count, char=None):
        char = char or '-'
        self.l_print(0, f'# {char*count}')

    def banner(self, label, width=None):
        width = width or 50
        self.blank_line(2)
        title = _expand_text(label.upper())
        _l = (width//2) - len(title)//2
        _l = max(_l, 0)
        self.l_print(0, f'# {"-"*width}')
        self.l_print(0, f'# {" ".ljust(_l)}{title}')
        self.l_print(0, f'# {"-"*width}')

    def sm_banner(self, label):
        self.banner(label=label, width=24)


def _expand_text(text):
    t = []
    for c in text:
        t.append(f'{c} ')
    return ''.join(t)


def _get_indent(level):
    return '' if level < 1 else ' '.ljust(level * 4)
