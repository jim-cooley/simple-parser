#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
import os
from enum import unique, IntEnum
from multiprocessing import SimpleQueue

from interpreter.focal import Focal
from interpreter.notation import FunctionalNotationPrinter
from interpreter.treeprint import print_forest, print_results
from runtime.dataframe import Dataset
from runtime.exceptions import getLogFacility, runtime_error
from runtime.options import getOptions
from runtime.pandas import print_dataframe
from runtime.runtime import load_file, find_file
from runtime.scope import Object
from test.suite_runner import _t_print


@unique
class SLOT(IntEnum):
    INVOKE = 0
    ARGC = 1
    HELP = 2


class FocalConsole:
    def __init__(self, options=None, file=None):
        self.focal = Focal(options, file=file)
        self.logger = getLogFacility('focal')
        self.option = getOptions('focal')
        self.environment = self.focal.environment

    def load(self, fname):
        verbose = self.option.verbose
        if verbose:
            print(f'\n\nloading {fname}...')
        source = load_file(self.find_file(fname))
        if not self.option.step_wise:
            self.parse(source)
        else:
            for line in source.splitlines():
                if line:
                    self.parse(line)

    def find_file(self, fname):
        fname = find_file(fname)
        ty = os.path.splitext(fname)[1]
        if ty == '.t':
            self.option.step_wise = True
        return fname

    def parse(self, lines):
        verbose = self.option.verbose
        if lines[0].startswith('%'):
            self.do_command(lines)
        else:
            if verbose:
                if self.option.step_wise:
                    print(f'parsing: {lines}')
                else:
                    print(f'parsing')
            target = self.focal.parse(lines)
            if verbose:
                print_forest(target, self.logger, label=None, print_results=verbose, print_notation=False)
            if self.option.auto_run:
                self.run(target)
            self.environment = target

    def run(self, target):
        if self.option.verbose:
            print(f'\nrunning:\n')
        target = self.focal.run()
        if self.option.verbose:
            stack_depth(self)
            print_results(target, self.logger)
            _print_symbols(target.scope)

    def go(self):
        if self.option.file is not None:
            self.load(self.option.file)
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
                    line = line[:len(line) - 1]
                    lines.append(line)
                    _continue = True
                    continue
                if line == 'exit' or line == 'exit()' or len(line) == 0:
                    _stop = True
                    break
                if line == 'help':
                    line = '%%help'
                if line.startswith('%'):
                    if not line.startswith('%%'):
                        line = '%' + line  # oh, this is so so common
                lines.append(line)
            if _stop:
                break
            lines = '\n'.join(lines).rstrip()
            self.parse(lines)

    # ---------------------
    # commands
    # ---------------------
    def do_command(self, source):
        lines = source.replace('\n', ';').replace('%', '').split(';')
        for line in lines:
            args = line.split(' ')
            command = args[0]
            if len(args) > 1:
                args = args[1:]
            else:
                args = []
            _dispatchCommand(self, command, args, 'commands')


# ---------------------
# dispatch
# ---------------------
def _dispatchCommand(console, cmd, args, disptab):
    if disptab not in _funcdesc_locator:
        runtime_error(f'dispatch table: {disptab} not found')

    descriptor = _funcdesc_locator[disptab]
    disptab = descriptor[0]
    aliases = descriptor[1]
    if cmd in aliases:
        cmd = aliases[cmd]
    if cmd in disptab:
        fndesc = disptab[cmd]
        argc = fndesc[SLOT.ARGC]
        fn = fndesc[SLOT.INVOKE]
        if argc > 0 and not args:
            runtime_error("Argument expected")
        return fn(console, args)
    else:
        print(f"Invalid Command: '{cmd}'\nType 'help' for help.")


# ---------------------
# base commands
# ---------------------

def do_break(console, args):
    breakpoint()


def do_help(console, args):
    cmd = args[0] if len(args) > 0 else 'command'
    if cmd not in _funcdesc_locator:
        cmd = 'commands'
    print("\n\n")
    _print_help_text('help')
    _print_commands(_funcdesc_locator[cmd], label=f'{cmd}:')


def do_load_script(console, args):
    fname = args[0]
    load_parse_script(console, fname)


def do_parse(console, args=None):
    source = console.environment.source
    console.environment = console.parser.parse(environment=console.environment, source=source)
    if console.option.verbose:
        show_tree(console)
    if console.option.auto_run:
        do_run(console)


def do_run(focal, args=None):
    focal.environment = focal.interpreter.apply(environment=focal.environment)  # execute script


# ---------------------
# print
# ---------------------
def do_print(console, vargs):
    logger = getLogFacility('focal')
    line = []
    for i in range(0, len(vargs)):
        o = vargs[i]
        if isinstance(o, Dataset):
            print_dataframe(o)
        else:
            if hasattr(o, 'format'):
                text = o.format()
            else:
                text = f'{o}'
            line.append(text)
    text = ' '.join(line)
    _t_print(logger, text)
    return vargs.message


# ---------------------
# options
# ---------------------
def set_options(console, args):
    option = args[0]
    if isinstance(option, Object):
        name = option.name
        if name in _set_aliases:
            name = _set_aliases[name]
        d = {name: option.value}
        _update_options(d)
    else:
        print(f"Unrecognized option: {option}")
    pass


def _to_efoptions(options):
    return options.dict(keys=['strict', 'force_errors'])


def _update_options(options):
    o = getOptions('focal')
    o.update(options)
    _update_logfacility_options(o)


def _update_logfacility_options(options):
    efo = _to_efoptions(options)
    logger = getLogFacility('focal')
    logger.set_options(efo)


# ---------------------
# show
# ---------------------
def do_show(console, args):
    cmd = args[0]
    _dispatchCommand(console=console, cmd=cmd, disptab='show', args=args[1:])


def show_aliases(console, args=None):
    _print_dictionary(_command_aliases, 'commands:')
    _print_dictionary(_set_aliases, 'set:')
    _print_dictionary(_show_aliases, 'show:')


def show_commands(console, args=None):
    _print_commands(_command_funcdesc, 'commands:')
    _print_commands(_show_funcdesc, 'show:')


def show_keywords(console, args=None):
    _print_keywords(console.environment.keywords)


def show_notation(console, args=None):
    printer = FunctionalNotationPrinter(indent=True)
    trees = console.environment.trees
    if trees is None or len(trees) < 1:
        return
    idx = 0
    for i in range(0, len(trees)):
        idx += 1
        t = trees[i]
        print(f'\ntree{idx}:')
        if t.root is None:
            print("<empty>")
            continue
        print(f'{printer.apply(t.root)}')


def show_options(console, args=None):
    d = console.option.dict()
    _print_dictionary(d, label="options", skip=['_defaults'])


def show_stack(console, args=None):
    stack = console.environment.stack
    _print_stack(console.environment.stack, label="stack")


def stack_depth(console, args=None):
    print(f'stack depth: {console.environment.stack.depth()}')


def show_symbols(console, args=None):
    _print_symbols(console.environment.scope)


def show_tokens(console, args=None):
    print('tokens:')
    if console.environment.tokens is not None:
        console.environment.tokens.printall()
    else:
        print("None")


def show_tree(console, args=None):
    env = console.environment
    # _print_banner("parse tree")
    print_forest(env, env.logger, label=None, print_results=console.option.verbose, print_notation=False)
    if console.option.verbose:
        _print_symbols(env.scope)


def show_sourcelines(console, args=None):
    _print_lines(console.environment.lines, "source")


# ---------------------
# Internal Commands
# ---------------------
# Internal Commands are commands that do not use 'args' but take regular parameters
def load_parse_script(console, fname):
    source = load_file(fname)
    console.environment.set_source(source)
    if console.option.auto_listback:
        show_sourcelines(console)
    if console.option.auto_parse:
        do_parse(console)


# ---------------------
# Helpers
# ---------------------
def error(message):
    logger = getLogFacility('lexer')
    logger.error(message)


def _print_help_text(key):
    key = 'help' if key is None else key
    key = 'help' if key not in _help_text else key
    _print_lines(_help_text[key], numbered=False)


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


# UNDONE: this is incorrect. Will print Post-Order
def _print_dictionary(d, label=None, skip=None, stringify=False, numbered=True):
    if label is not None:
        print(f"\n{label}: ")
    idx = 0
    skip = skip or []
    q = SimpleQueue()
    q.put(d)
    while not q.empty():
        s = q.get()
        for k in s:
            if k not in skip:
                v = s[k]
                if type(v).__name__ == 'Object':
                    q.put(v)
                if stringify:
                    if hasattr(v, 'name'):
                        v = v.name
                    v = f'{v}'
                if numbered:
                    print(f'{idx:5d}:  `{k}` = {v}')
                else:
                    print(f'`{k}` = {v}')
                idx += 1

    # UNDONE: Strip ;self'
    def _print_dict(self, d, numbered=False):
        _s = d
        if not _s:
            return
        if isinstance(_s, dict):
            print("{", numbered=numbered)
            self.indent()
            for key in _s:
                _v = _s[key]
                if isinstance(_v, dict) or isinstance(_v, list):
                    self.print("{ " f'{key}: ', numbered=numbered, end='')
                    self._print_dict(_v, numbered=numbered)
                else:
                    self.print("{ " f'{key}: {_v}' " },", numbered=numbered)
            self.dedent()
            if isinstance(_s, list):
                self.print("]", numbered=numbered)
            else:
                self.print("}", numbered=numbered)
        elif isinstance(_s, list):
            self.indent()
            self.print("[", numbered=numbered, append=True)
            for _v in _s:
                self.print(f'{_v}, ', numbered=numbered)
            self.dedent()
            self.print("]},", numbered=numbered)


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


def _print_stack(stack, label=None):
    if label is not None:
        print(f"\n{label}: ")
    print(f'stack depth: {stack.depth()}')
    if not stack.is_empty():
        idx = 1
        while idx <= stack.depth():
            item = stack.peek(-idx)
            print(f'{idx:5d}:  {item}')
            idx += 1


def _print_symbols(scope):
    print("\n\nsymbols: ")
    if scope is None:
        print('None')
    else:
        idx = 0
        q = SimpleQueue()
        q.put(scope)
        while not q.empty():
            s = q.get()
            if s._members is None or len(s._members) == 0:
                continue
            if hasattr(s, 'token'):
                print(f'\nscope: {s.token.lexeme}')
            else:
                print(f'\nglobal scope:')
            for k in s._members.keys():
                v = s._members[k]
                if type(v).__name__ == 'Object':
                    q.put(v)
                    print(f'{idx:5d}:  `{k}`: {v.qualname} : Object({v.token})')
                    idx += 1


def _print_keywords(scope):
    if scope._members is None or len(scope._members) == 0:
        return
    print(f'\nkeywords:')
    idx = 0
    for k in scope._members.keys():
        v = scope._members[k]
        if type(v).__name__ == 'Token':
            print(f'{idx:5d}:  `{k}`: {v}')
            idx += 1


# ---------------------
# command table
# ---------------------
# these are function descriptors for the intrinsic functions
# the format is (invoke_fn, init_fn)
_command_funcdesc = {
    'break': (do_break, 0, 'break into the debugger'),
    'help': (do_help, 0, 'print help info on commands'),
    'load': (do_load_script, 1, 'load script file'),
    'options': (show_options, 1, 'show options'),
    'parse': (do_parse, 0, 'parse loaded script'),
    'print': (do_print, 1, 'print'),
    'run': (do_run, 0, 'run interpreter'),
    'set': (set_options, 1, 'set options'),
    'show': (do_show, 1, 'show various things, see `help show`'),
    'show.stack': (do_show, 0, 'display the stack'),
}

_command_aliases = {
    'h': 'help',
    'opt': 'options',
    'p': 'print',
    's': 'show',
}

_show_funcdesc = {
    # functions:
    'aliases': (show_aliases, 0, 'list aliases for commands'),
    'keywords': (show_keywords, 0, 'display the keyword table for the current context'),
    'notation': (show_notation, 0, 'show the notation for commands before they are executed'),
    'options': (show_options, 0, 'show options'),
    'source': (show_sourcelines, 0, 'print out the current source'),
    'stack': (show_stack, 0, 'show information related to the stack (see `help stack`, or `help show.stack`'),
    'stack_depth': (stack_depth, 0, 'display stack depth'),
    'symbols': (show_symbols, 0, 'display the symbol table for the current context'),
    'tokens': (show_tokens, 0, 'display the tokens for the current source'),
    'tree': (show_tree, 0, 'display the current parse tree(s)'),
}

_set_aliases = {
    'al': 'auto_listback',
    'ap': 'auto_parse',
    'ar': 'auto_run',
    'e': 'throw_errors',
    'f': 'force_errors',
    'log': 'log_filename',
    'no.run': 'no_run',
    'nr': 'no_run',
    'print.tokens': 'print_tokens',
    'strict': 'strict',
    'throw': 'throw_errors',
    'tk': 'print_tokens',
    'tokens': 'print_tokens',
    'v': 'verbose',
}

_show_aliases = {
    'a': 'aliases',
    'n': 'notation',
    'o': 'options',
    'sd': 'stack_depth',
    'stack.depth': 'stack_depth',
}

_funcdesc_locator = {
    'commands': (_command_funcdesc, _command_aliases),
    'show': (_show_funcdesc, _show_aliases),
}

_help_text = {
    'help': ["Focal is a formulaic language and this is a console for it.",
             "To enter and run Focal language, simply enter your expression.  To invoke interpreter commands,",
             "use '%%' to prefix the commands, as is '%%help', or 'x = 5'.\n"]
}
