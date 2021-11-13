#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
from argparse import ArgumentParser

from interpreter.shell import CommandShell
from interpreter.fixups import Fixups
from interpreter.interpreter import Interpreter
from parser.parser import Parser
from runtime.environment import Environment
from test.suite_runner import _dump_environment

LOG_FILE = './focal.log'


class FocalConsole:
    def __init__(self, options, file):
        self.environment = Environment(file=file)
        self.logger = self.environment.logger
        self.parser = Parser(self.environment, verbose=False)
        self.fixups = Fixups(self.environment)
        self.interp = Interpreter(self.environment)
        self.command = CommandShell(self.environment)
        self.options = options
        if options is not None:
            self.environment.update_options(vars(options))

    def parse(self, line):
        command = False
        source = self.environment.source
        if line.startswith('%%'):
            command = True
        parse_trees = self.fixups.apply(self.parser.parse(text=line, command=command))
        self.environment.trees = parse_trees
        if command:
            self.environment.source = source
        return parse_trees

    def run(self, trees=None):
        if trees is not None:
            self.environment.trees = trees
        self.command.execute(self.interp)

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
            tree = self.parse(lines)
            self.run(tree)
