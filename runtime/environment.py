from dataclasses import dataclass

from runtime import exceptions
from runtime.exceptions import getLogFacility
from runtime.indexdict import IndexedDict
from runtime.keywords import Keywords
from runtime.options import getOptions
from runtime.scope import Scope

from runtime.stack import RuntimeStack
from runtime.version import VERSION


@dataclass
class Environment:
    """
    Environment maintains the parse tree and execution environment state
    Centralized exception handling also flows through as it is aware of options.

    Environment.current is a global reference to the environment
    """
    current = None

    def __init__(self, keywords=None):
        self.keywords = keywords if keywords is not None else Keywords()
        self.globals = Scope(parent_scope=self.keywords)
        self.scope = self.globals
        self.commands = []
        self.trees = []
        self.lines = None
        self.source = None
        self.tokens = None
        self.logger = getLogFacility('focal')
        self.stack = RuntimeStack()
        self.version = VERSION
        Environment.current = self

    def get_logger(self):
        return self.logger

    def close(self):
        if self.logger:
            self.logger.close()
            exceptions.removeLogFacility(self.logger)
            self.logger = None

    @staticmethod
    def enter(scope=None):
        if scope is None:
            scope = Scope(Environment.current.scope)
        if scope.parent_scope is None:
            scope.parent_scope = Environment.current.scope
        Environment.current.scope = scope
        return scope

    def get_line(self, line):
        if line < len(self.lines):
            return self.lines[line]
        return ''

    @staticmethod
    def leave():
        scope = Environment.current.scope
        parent = scope.parent_scope
        Environment.current.scope = parent
        return scope

    def set_source(self, source):
        self.source = source
        self.lines = source.splitlines(True)
        return source

    def print_line(self, line):
        print(self.get_line(line))


def _get_line(loc, lines):
    if loc.line < len(lines):
        return lines[loc.line]
    return ''
