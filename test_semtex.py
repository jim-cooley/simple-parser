#!./bin/python3
# test semantic analysis
import sys
from abc import ABC

from environment import Environment
from fixups import Fixups
from interpreter import Interpreter
from parser import Parser
from test.suite_runner import TestSuiteRunner, _dump_trees, _t_print, _log_exception, _dump_environment
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
    'regression',
    'errors',
    'simple',
]


class SemanticAnalysisTestRunner(TestSuiteRunner, ABC):

    def __init__(self, test_data, skip_tests=None):
        super().__init__(test_data, skip_tests, log_dir='./etc/test/log/semtex')
        self.verbose = False

    def run_unprotected_test(self, log, name, test):
        environment = Environment()
        parser = Parser(environment, verbose=False)
        fixups = Fixups(environment)
        interp = Interpreter(environment)
        trees = fixups.apply(parser.parse(text=test))
        if self.verbose:
            _dump_environment(environment, log, label='post')
        interp.apply(trees)
        _dump_environment(environment, log, label='post')


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
