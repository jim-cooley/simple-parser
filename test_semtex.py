#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
# test semantic analysis
import sys
from abc import ABC

from interpreter.shell import CommandShell
from interpreter.fixups import Fixups
from interpreter.interpreter import Interpreter
from parser.parser import Parser
from runtime.exceptions import getLogFacility
from test.suite_runner import TestSuiteRunner, _dump_environment
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
    'regression',
    'regress',

    'assignment',
    'binops',
    'blocks',
#   'boolean',
#   'boolean_var',
    'commands',
#   'constant_expr',
    'declaration',
    'declarations_multiline',
#   'duration',
    'empty_sets',
    'eval_sequences',
    #'eval_test',
    'expressions',
    'functions',
    #'grouping',
    'identifiers',
    'indexed_properties',
    'indexing',
    'keywords',
    'language',
    'language_expr',
    'lifting',
    'lists',
    'none',
    'parameters',
    #'prime',
    'properties',
    'ranges',
    'sequences',
    #'set_operations',
    #'set_parameters',
    #'set_unary',
    #'sets',
    'shell',
    'simple',
    'simple2',
    'simpler',
    'statements',
    'system1',
    'system2',
    #'time',
    'trading',
    #'tuples',
    #'unary',
    'var',
]


class SemanticAnalysisTestRunner(TestSuiteRunner, ABC):

    def __init__(self, test_data, skip_tests=_skip_tests):
        super().__init__(test_data, skip_tests, log_dir='./etc/test/log/focal')
        self.verbose = True
        self.test = True

    def run_unprotected_test(self, environment, name, test):
        logger = getLogFacility('focal')
        parser = Parser()
        fixups = Fixups()
        interp = Interpreter()
        command = CommandShell(parser=parser, interpreter=interp)
        environment = fixups.apply(parser.parse(source=test))
        if self.verbose:
            _dump_environment(environment, label='post', print_tokens=False, print_results=False)
        logger.banner("RUN")
        environment = command.run(target=environment)
        if self.test:
            _dump_environment(environment, label='post',
                              print_tokens=False, print_trees=False, print_results=True, print_symbols=True,
                              print_commands=False)


# this is only for execution under debugger or via command-line
if __name__ == '__main__':
    args = sys.argv[1:]

    runner = SemanticAnalysisTestRunner(test_data, _skip_tests)

    # short-circuit for debugging
    _test_suite = True
    if not _test_suite:
        runner.interactive = True
        runner.run_suites([
            'set_operations',
        ])

    # test suite
    else:
        if len(args) > 0:
            runner.run_suites(args)
        else:
            runner.run_full_pass()
