from dataclasses import dataclass
from enum import Enum

from exceptions import ExceptionReporter
from keywords import Keywords
from scope import Scope


#
# Environment maintains the parse tree and execution environment state
# Centralized exception handling also flows through as it is aware of options.
#

# option_strict forces variables to be defined before they are used
DEFAULT_OPTION_STRICT = False

# option_force_errors forces warnings into errors
DEFAULT_FORCE_ERRORS = False


@dataclass
class Environment(object):
    current = None

    class OPTIONS(Enum):
        STRICT = 'strict'
        FORCE_ERRORS = 'force_errors'

    def __init__(self, source=None, nodes=None, commands=None, keywords=None, options=None):
        self.keywords = keywords if keywords is not None else Keywords()
        self.globals = Scope(self.keywords)
        self.symbols = self.globals
        self.commands = commands if commands is not None else []
        self.trees = []
        self.lines = None
        self.source = self.set_source(source) if source is not None else None
        self.tokens = None
        self.options = options if options is not None else {}
        self.logger = ExceptionReporter(self)
        Environment.current = self

    def __getitem__(self, key):
        if key in self.options or key in _option_defaults:
            return self._get_option(key, _get_default(key, False))

    def __missing__(self, key):
        if key in _option_defaults:
            return _get_default(key, False)

    def __setitem__(self, key, value):
        if key in self.options or key in _option_defaults:
            self.options[key] = value
        else:
            super().__setattr__(key, value)

    def get_logger(self):
        return self.logger

    @staticmethod
    def get_logger():
        return Environment.current.logger

    def _get_option(self, key, default):
        if key not in self.options:
            return default
        return self.options[key]

    def set_source(self, source):
        self.source = source
        self.lines = source.splitlines(True)
        return source

    def enter(self, scope=None):
        if scope is None:
            scope = Scope()
        scope.link(Environment.current.symbols)
        Environment.current.symbols = scope
        return scope

    def leave(self, scope):
        parent = scope.parent_scope
        Environment.current.symbols = parent
        return scope

    def get_line(self, line):
        if line < len(self.lines):
            return self.lines[line]
        return ''

    def print_line(self, line):
        print(self.get_line(line))


_option_defaults = {
    Environment.OPTIONS.STRICT: DEFAULT_OPTION_STRICT,
    Environment.OPTIONS.FORCE_ERRORS: DEFAULT_FORCE_ERRORS,
}


def _get_default(key, default):
    return default if key not in _option_defaults else _option_defaults[key]


def _get_line(loc, lines):
    if loc.line < len(lines):
        return lines[loc.line]
    return ''
