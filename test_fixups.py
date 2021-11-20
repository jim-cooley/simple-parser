#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
# test semantic analysis
import sys
from abc import ABC

from interpreter.fixups import Fixups
from parser.parser import Parser
from test.suite_runner import TestSuiteRunner, _dump_environment
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
    'regression',
    'regress',
    'simple'
]


class SemanticAnalysisTestRunner(TestSuiteRunner, ABC):

    def __init__(self, test_data, skip_tests=None):
        super().__init__(test_data, skip_tests, log_dir='./etc/test/log/fixups')

    def run_unprotected_test(self, environment, name, test):
        parser = Parser()
        fixups = Fixups()
        environment = parser.parse(source=test)
        _dump_environment(environment, print_results=False, print_tokens=False, print_symbols=False)
        environment = fixups.apply(environment)
        _dump_environment(environment, label='post', print_results=True, print_tokens=False, print_trees=True,
                          print_symbols=False)


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
