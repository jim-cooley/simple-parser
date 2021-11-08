#!./bin/python3
# test semantic analysis
import sys
from abc import ABC

from fixups import Fixups
from interpreter import Interpreter
from parser import Parser
from notation import NotationPrinter
from test.suite_runner import TestSuiteRunner, _log_exception
from environment import _t_print
from treeprint import print_forest
from test.test_setup import test_data

_test_suite = True       # False is useful for debugging, interactive.  True for test suites
_skip_tests = [
]


class PostfixPrinterRunner(TestSuiteRunner, ABC):

    def __init__(self, test_data, skip_tests=None):
        super().__init__(test_data, skip_tests, log_dir='./etc/test/log/postfix')

    def run_unprotected_test(self, environment, name, test):
        parser = Parser(str=test, verbose=False)
        printer = NotationPrinter()
        parse_tree = parser.parse()
        idx = 0
        for t in parse_tree.root:
            idx += 1
            print(f'{idx:5d}: {printer.apply(t)}')


# this is only for execution under debugger or via command-line
if __name__ == '__main__':
    args = sys.argv[1:]

    runner = PostfixPrinterRunner(test_data, _skip_tests)

    # short-circuit for debugging
    _test_suite = True
    if not _test_suite:
        runner.interactive = True
        runner.run_suites([
            'system2',
        ])

    # test suite
    else:
        if len(args) > 0:
            runner.run_suites(args)
        else:
            runner.run_full_pass()
