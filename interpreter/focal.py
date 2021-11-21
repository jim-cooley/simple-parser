from interpreter.fixups import Fixups
from interpreter.interpreter import Interpreter
from interpreter.treeprint import print_forest
from parser.parser import Parser
from runtime.environment import Environment
from runtime.exceptions import getLogFacility, runtime_error, runtime_warning
from runtime.options import getOptions


_option_defaults = {
    'auto_listback': True,  # automatically show source after load
    'auto_parse': True,     # automatically parse upon load
    'auto_run': True,       # automatically run after parsing
    'file': None,           # auto run a script file
    'force_errors': False,  # option_force_errors forces warnings into errors
    'log_filename': './focal.log',
    'no_run': False,
    'print_tokens': False,
    'step_wise': False,     # console: run line by line (for test scripts)
    'strict': False,        # option_strict forces variables to be defined before they are used
    'throw_errors': True,
    'verbose': True,
}


class Focal:
    def __init__(self, options=None, file=None):
        self.logger = getLogFacility('focal', lines=None, file=file)
        self.option = getOptions('focal', options=vars(options), defaults=_option_defaults)
        self.fixups = Fixups()
        self.parser = Parser()
        self.interpreter = Interpreter()
        self.environment = Environment()         # target environment
        self.logger.set_lines = self.environment.lines

    def parse(self, source):
        target = self.environment
        self.environment = self.fixups.apply(self.parser.parse(target, source=source))
        return self.environment

    def run(self):
        try:
            target = self.environment
            self.environment = self.interpreter.apply(target)  # execute script
            return self.environment
        except Exception as e:
            if self.option.throw_errors:
                runtime_error(f'{e}')
            else:
                runtime_warning(f'{e}')

