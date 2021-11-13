from dataclasses import dataclass

from runtime import exceptions
from runtime.exceptions import getLogFacility
from runtime.indexdict import IndexedDict
from runtime.keywords import Keywords
from runtime.scope import Scope

from runtime.stack import RuntimeStack
from runtime.version import VERSION

_option_defaults = {
    'strict': False,    # option_strict forces variables to be defined before they are used
    'force_errors': False,  # option_force_errors forces warnings into errors
    'throw_errors': True,
    'verbose': False,
}


@dataclass
class Environment(object):
    """
    Environment maintains the parse tree and execution environment state
    Centralized exception handling also flows through as it is aware of options.

    Environment.current is a global reference to the environment
    """
    current = None

    def __init__(self, source=None, commands=None, keywords=None, options=None, file=None):
        self.keywords = keywords if keywords is not None else Keywords()
        self.globals = Scope(parent_scope=self.keywords)
        self.scope = self.globals
        self.commands = commands if commands is not None else []
        self.trees = []
        self.interpreter = None
        self.parser = None
        self.lines = None
        self.source = self.set_source(source) if source is not None else None
        self.tokens = None
        self.options = IndexedDict(items=options, defaults=_option_defaults)
        self.logger = getLogFacility('semtex', env=self, file=file)
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
            scope = Scope()
        scope.link(Environment.current.scope)
        Environment.current.scope = scope
        return scope

    def get_line(self, line):
        if line < len(self.lines):
            return self.lines[line]
        return ''

    @staticmethod
    def leave(scope=None):
        scope = Environment.current.scope if scope is None else scope
        parent = scope.parent_scope
        Environment.current.scope = parent
        return scope

    def set_source(self, source):
        self.source = source
        self.lines = source.splitlines(True)
        return source

    def to_efoptions(self):
        return self.options.to_dict(keys=['strict', 'force_errors'])

    def update_options(self, options):
        self.options.update(options)
        self._update_options_actions()

    def _update_options_actions(self):
        efo = self.to_efoptions()
        self.logger.set_options(efo)

    def print_line(self, line):
        print(self.get_line(line))


def _get_line(loc, lines):
    if loc.line < len(lines):
        return lines[loc.line]
    return ''
