from argparse import ArgumentParser
from enum import IntEnum, unique

from parser.lexer import Lexer
from parser.tokenstream import TokenStream
from runtime.exceptions import getLogFacility
from runtime.options import getOptions
from runtime.runtime import load_file


_help_text = {
    'help': ["Focal is a formulaic language and this is a console for it.",
             "To enter and run Focal language, simply enter your expression.  To invoke interpreter commands,",
             "use '%%' to prefix the commands, as is '%%help', or 'x = 5'.\n"]
}
_option_defaults = {
    'file': None,           # auto run a script file
    'single_line': True,
    'verbose': True,
}

LOG_FILE = './lexer.log'


@unique
class SLOT(IntEnum):
    INVOKE = 0
    HELP = 1


class LexConsole:
    def __init__(self, options=None, file=None):
        self.logger = getLogFacility('lexer', lines=None, file=file)
        self.option = getOptions('lexer', options=vars(options), defaults=_option_defaults)
        pass

    def load(self, fname):
        if self.option.verbose:
            print(f'\n\nloading {fname}...')
        source = load_file(fname)
        return self.lex(source)

    def lex(self, source):
        if self.option.single_line:
            lines = source.splitlines()
        else:
            lines = source
        for line in lines:
            lexer = TokenStream(source=line)
            print('\n\nsource:')
            print(line)
            print('tokens:')
            lexer.printall()
        return source

    def go(self):
        if self.option.file is not None:
            fname = self.option.file
            source = self.load(fname)
        _stop = False
        while not _stop:
            lines = []
            _start = True
            _continue = True
            while _continue:
                _continue = False
                if _start:
                    _start = False
                    print("\n\n>> ", end='')
                else:
                    print("   ", end='')
                line = input()
                if line.endswith('\\') or line.endswith('_'):
                    line = line[:len(line)-1]
                    lines.append(line)
                    _continue = True
                    continue
                if line == 'exit' or line == 'exit()' or len(line) == 0:
                    _stop = True
                    break
                if line == 'help':
                    line = '%help'
                lines.append(line)
            if _stop:
                break
            if lines[0].startswith('%'):
                do_command(self, lines[0])
            else:
                source = '\n'.join(lines).rstrip()
                self.lex(source)


# ---------------------
# dispatch
# ---------------------
def _dispatchCommand(console, cmd, args, disptab):
    if disptab not in _funcdesc_locator:
        error(f'dispatch table: {disptab} not found')

    descriptor = _funcdesc_locator[disptab]
    disptab = descriptor[0]
    aliases = descriptor[1]
    if cmd in aliases:
        cmd = aliases[cmd]
    if cmd in disptab:
        fndesc = disptab[cmd]
        fn = fndesc[SLOT.INVOKE]
        return fn(console, args)


# ---------------------
# commands
# ---------------------
def do_command(console, command):
    args = command.replace('%', '').split(' ')
    command = args[0]
    if len(args) > 1:
        args = args[1:]
    else:
        args = []
    _dispatchCommand(console, command, args, 'commands')


def do_help(console, args):
    cmd = 'commands'
    if args is not None:
        if len(args) > 0:
            cmd = args[0]
    if cmd not in _funcdesc_locator:
        cmd = 'commands'
    print("\n\n")
    _print_help_text('help')
    _print_commands(_funcdesc_locator[cmd], label=f'{cmd}')


def do_load_script(console, args):
    if len(args) < 1:
        error("load script requires a file name")
    console.load(args[0])


# ---------------------
# helpers
# ---------------------
def error(message):
    logger = getLogFacility('lexer')
    logger.error(message)


def _print_commands(locator, label=None):
    if label is not None:
        print(f"\n{label}: ")
    table = locator[0]
    aliases = locator[1]
    idx = 0
    for cmd in table:
        fndesc = table[cmd]
        print(f'{idx:5d}:  `{cmd}`: {fndesc[SLOT.HELP]}')
        idx += 1


def _print_help_text(key):
    key = 'help' if key is None else key
    key = 'help' if key not in _help_text else key
    _print_lines(_help_text[key], numbered=False)


def _print_lines(lines, label=None, numbered=True):
    if label is not None:
        print(f"\n{label}: ")
    idx = 0
    for line in lines:
        if numbered:
            print(f'{idx:5d}:  {line.rstrip()}')
        else:
            print(f'{line.rstrip()}')
        idx += 1


# ---------------------
# command table
# ---------------------
_command_funcdesc = {
    'help': (do_help, 'print help info on commands'),
    'load': (do_load_script, 'load script file'),
}

_command_aliases = {
    'h': 'help',
    'l': 'load',
}

_funcdesc_locator = {
    'commands': (_command_funcdesc, _command_aliases),
}


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-f', '--file', default=None, help="script file to execute")
    parser.add_argument('file', nargs='?', default=None, help="script file to execute")
    parser.add_argument('-l', '--single_line', dest='single_line', action='store_true', help='parse 1 line at a time')
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', help="less verbose output")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="more verbose output")
    parser.set_defaults(verbose=False, single_line=True)
    args = parser.parse_args()

    with open(LOG_FILE, 'w') as log:
        lexer = LexConsole(args, file=log)
        lexer.go()
