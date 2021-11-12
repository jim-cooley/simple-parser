#!/Volumes/HD2/Lab/Repository/jimc/python3.9/bin/python3
import sys
from abc import ABC

from test.suite_runner import TestSuiteRunner, _log_exception, _dump_environment
from parser.parser import Parser
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
    'regression',
    'regress',
    'simple'
]


class ParserTestRunner(TestSuiteRunner, ABC):

    def __init__(self, td, skip_tests=None):
        super().__init__(td, skip_tests, log_dir='./etc/test/log/parser')

    def run_unprotected_test(self, environment, name, test):
        parser = Parser(environment)
        parser.parse(text=test)
        _dump_environment(environment, print_results=False)


# this is only for execution under debugger or via command-line
if __name__ == '__main__':
    args = sys.argv[1:]
    runner = ParserTestRunner(test_data, _skip_tests)

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
