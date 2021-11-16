#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
from argparse import ArgumentParser

from interpreter.shell import CommandShell, load_script_file, show_tree, _print_symbols
from interpreter.fixups import Fixups
from interpreter.interpreter import Interpreter
from interpreter.treeprint import print_forest
from parser.parser import Parser
from runtime.environment import Environment
from runtime.exceptions import getLogFacility
from runtime.options import getOptions
from runtime.runtime import load_script

_option_defaults = {
    'auto_listback': True,  # automatically show source after load
    'auto_parse': True,     # automatically parse upon load
    'auto_run': True,       # automatically run after parsing
    'file': None,           # auto run a script file
    'force_errors': False,  # option_force_errors forces warnings into errors
    'log_filename': './focal.log',
    'no_run': False,
    'print_tokens': False,
    'strict': False,        # option_strict forces variables to be defined before they are used
    'throw_errors': True,
    'verbose': True,
}


class FocalConsole:
    def __init__(self, options=None, file=None):
        self.logger = getLogFacility('focal', lines=None, file=file)
        self.option = getOptions('focal', options=vars(options), defaults=_option_defaults)
        self.fixups = Fixups()
        self.parser = Parser()
        self.focal = Interpreter()
        self.shell = CommandShell(parser=self.parser, interpreter=self.focal)
        self.environment = Environment()
        self.target = Environment()         # target environment
        self.logger.set_lines = self.target.lines

    def load(self, fname):
        verbose = self.option.verbose
        if verbose:
            print(f'\n\nloading {fname}...')
        source = load_script(fname)
        if verbose:
            print(f'parsing {fname}')
        environment = self.parse(source)
        if verbose:
            print_forest(environment, self.logger, label=None, print_results=verbose, print_notation=False)
        if self.option.auto_run:
            if verbose:
                print(f'\nrunning {fname}:\n')
                self.run(environment)
                _print_symbols(environment.scope)
            else:
                self.run(environment)

    def parse(self, source):
        if source.startswith('%%'):
            environment = self.environment
            environment = self.fixups.apply(self.parser.parse(environment=environment, source=source))
            self.environment = environment
        else:
            environment = self.target
            environment = self.fixups.apply(self.parser.parse(environment, source=source))
            self.target = environment
        return environment

    def run(self, environment):
        self.shell.run(target=self.target)

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

