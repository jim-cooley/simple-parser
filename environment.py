from collections import deque
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
class RuntimeStack(object):
    def __init__(self):
        self._stack = deque()

    def is_empty(self):
        return True if len(self._stack) == 0 else False

    def depth(self):
        return len(self._stack)

    def top(self):
        return self._stack[-1]

    def push(self, x):
        self._stack.append(x)

    def push_all(self, l):
        for item in l:
            self.push(item)

    def pop(self):
        if self.is_empty():
            Environment.get_logger().runtime_error(f'Stack underflow', loc=None)
        return self._stack.pop()

    def clear(self):
        self._stack.clear()
        self._stack = deque()


@dataclass
class Environment(object):
    current = None

    class OPTIONS(Enum):
        STRICT = 'strict'
        FORCE_ERRORS = 'force_errors'

    def __init__(self, source=None, commands=None, keywords=None, options=None):
        self.keywords = keywords if keywords is not None else Keywords()
        self.globals = Scope(self.keywords)
        self.scope = self.globals
        self.commands = commands if commands is not None else []
        self.trees = []
        self.lines = None
        self.source = self.set_source(source) if source is not None else None
        self.tokens = None
        self.options = options if options is not None else {}
        self.logger = ExceptionReporter(self)
        self.stack = RuntimeStack()
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

    @staticmethod
    def enter(scope=None):
        if scope is None:
            scope = Scope()
        scope.link(Environment.current.scope)
        Environment.current.scope = scope
        return scope

    @staticmethod
    def leave(scope=None):
        scope = Environment.current.scope if scope is None else scope
        parent = scope.parent_scope
        Environment.current.scope = parent
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
