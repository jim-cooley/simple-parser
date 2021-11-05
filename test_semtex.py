#!./bin/python3
# test semantic analysis
import sys
from abc import ABC

from command_interpreter import CommandInterpreter
from environment import Environment, _t_print
from fixups import Fixups
from interpreter import Interpreter
from parser import Parser
from test.suite_runner import TestSuiteRunner, _log_exception, _dump_environment
from treeprint import print_forest
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
    'regression',
    'regress',

#   'assignment',
    'binops',
#   'blocks',
#   'boolean',
    'boolean_var',
    'commands',
#   'constant_expr',
#   'declaration',
    'declarations_multiline',
#   'duration',
    'empty_sets',
    #'eval_sequences',
    #'eval_test',
    'expressions',
    'functions',
    'grouping',
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
    'prime',
    #'properties',
    #'ranges',
    #'sequences',
    'set_operations',
    'set_parameters',
    'set_unary',
    'sets',
    'shell',
    'simple',
    'simple2',
    'simpler',
    'statements',
    'system1',
    'system2',
    'time',
    'trading',
    'tuples',
    'unary',
    'var',
]


class SemanticAnalysisTestRunner(TestSuiteRunner, ABC):

    def __init__(self, test_data, skip_tests=None):
        super().__init__(test_data, skip_tests, log_dir='./etc/test/log/semtex')
        self.verbose = True
        self.test = False

    def run_unprotected_test(self, log, name, test):
        environment = Environment()
        parser = Parser(environment, verbose=False)
        fixups = Fixups(environment)
        interp = Interpreter(environment)
        command = CommandInterpreter(environment)
        environment.trees = fixups.apply(parser.parse(text=test))
        if self.verbose:
            _dump_environment(environment, log, label='post', print_tokens=False)
        print('\n-----------------------------------------------')
        print('                    R U N')
        print('-----------------------------------------------\n')
        command.execute(interp)
#       interp.apply(trees)
        if self.test:
            _dump_environment(environment, log, label='post', print_results=True, print_symbols=True)


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
