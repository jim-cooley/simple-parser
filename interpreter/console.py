#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
from argparse import ArgumentParser

from interpreter.shell import CommandShell
from interpreter.fixups import Fixups
from interpreter.interpreter import Interpreter
from parser.parser import Parser
from runtime.environment import Environment
from runtime.exceptions import getLogFacility
from runtime.options import getOptions


_option_defaults = {
    'strict': False,    # option_strict forces variables to be defined before they are used
    'force_errors': False,  # option_force_errors forces warnings into errors
    'throw_errors': True,
    'print_tokens': False,
    'no_run': False,
    'verbose': False,
    'log_filename': './focal.log'
}

CONSOLE_LOG = './focal_console.log'


class FocalConsole:
    def __init__(self, options=None, file=None):
        self.logger = getLogFacility('focal', env=self, file=file)
        self.options = getOptions('focal', options=vars(options), defaults=_option_defaults)
        self.fixups = Fixups()
        self.parser = Parser()
        self.focal = Interpreter()
        self.shell = CommandShell(self.focal)
        self.target = None   # target environment

    def parse(self, lines):
        if lines.startswith('%%'):
            # this causes the parser to create a new environment for each command and throw them away
            environment = self.fixups.apply(self.parser.parse(environment=None, source=lines))
        else:
            # this causes the parser to re-use the same environment each time for focal-related work
            environment = self.target
            environment = self.fixups.apply(self.parser.parse(environment, source=lines))
            self.target = environment
        return environment

    def run(self, environment):
        self.shell.execute(environment, self.focal)

    def go(self):
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
                    line = '%%help'
                if line.startswith('%'):
                    if not line.startswith('%%'):
                        line = '%' + line           # oh, this is so so common
                lines.append(line)
            if _stop:
                break
            lines = '\n'.join(lines).rstrip()
            env = self.parse(lines)
            self.run(env)

