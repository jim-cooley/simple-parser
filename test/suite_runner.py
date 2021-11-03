import os
import traceback
from abc import abstractmethod, ABC

from exceptions import _t_print
from environment import _get_line
from notation import NotationPrinter
from scope import _dump_symbols
from treeprint import print_forest, print_node

_LOG_DIRECTORY = "./etc/test/log"
_SCRIPT_SEARCH_PATH = [
    ".",
    "./test/cases",
    "./etc/test",
    "../etc/test",
]


class TestSuiteRunner(ABC):

    def __init__(self, test_data, skip_tests=None, prefix='', log_dir=None, env=None):
        self.tests = test_data
        self.skip_tests = skip_tests if skip_tests is not None else []
        self.prefix = prefix
        self.interactive = False
        self.environment = env
        self.logs_dir = log_dir if log_dir is not None else _LOG_DIRECTORY

    @abstractmethod
    def run_unprotected_test(self, log, name, test):
        pass

    def run_protected_test(self, log, name, test):
        try:
            self.run_unprotected_test(log, name, test)
        except Exception as e:
            _log_exception(e, log, name)

    def run_suites(self, suites):
        for name in suites:
            self.run_suite(name)

    def run_full_pass(self):
        for suite in self.tests.keys():
            if suite not in self.skip_tests:
                self.run_suite(suite)

    def run_suite(self, name):
        if name not in self.tests:
            fname = _find_test_file(name, _SCRIPT_SEARCH_PATH)
            self.run_test_script(fname)
            return
        print(f'\n\nsuite: {name}')
        cases = self.tests[name]
        if type(cases).__name__ == "list":
            idx = 0
            for test in cases:
                idx += 1
                self._run_single_test(name, test, idx)
            return
        else:
            fname = _find_test_file(name, _SCRIPT_SEARCH_PATH)
            self.run_test_script(fname)

    def run_test_script(self, fname):
        name = os.path.splitext(os.path.basename(fname))[0]
        tt = os.path.splitext(fname)[1]
        idx = 0
        with open(fname, 'r') as file:
            print(f'{fname}')
            test = file.read()
            if tt == '.t':
                for line in test.splitlines():
                    idx += 1
                    self._run_single_test(name, line, idx)
            else:
                self._run_single_test(name, test)

    def _run_single_test(self, name, test, idx=None):
        fn = f'{name}.log' if idx is None else f'{name}_{idx}.log'
        label = f'test:\n"{test}"' if idx is None else f'test: {idx}:\n"{test}"'
        fname = f'{self.logs_dir}/{self.prefix}{fn}'
        with open(fname, 'w') as log:
            _t_print(log, f'\n\n{label}')
            if not self.interactive:
                self.run_protected_test(log, name, test)
            else:
                self.run_unprotected_test(log, name, test)

    def _generate_empty_log(self, name, test, message='', idx=None):
        fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
        label = f'test:\n"{test}"' if idx is None else f'test: {idx}:\n"{test}"'
        with open(f'{self.logs_dir}/{fname}', 'w') as log:
            _t_print(log, message)


def _find_test_file(name, search_paths):
    for path in search_paths:
        fname = f'{path}/{name}'
        if os.path.isfile(fname):
            return fname
        if os.path.isfile(f'{fname}.p'):
            return f'{fname}.p'
        if os.path.isfile(f'{fname}.t'):
            return f'{fname}.t'
        if os.path.isfile(f'{fname}.f'):
            return f'{fname}.f'
    raise IOError(f'invalid test suite: {name}, is not a test file')


def _log_exception(e, log, name):
    trace = traceback.format_exc()
    _t_print(log, f'FAIL: \'{name}\' failed with Exception {e}\n')
    if trace is not None:
        print(f'{trace}')


def _dump_environment(env, log=None, label=None,
                      print_results=True,
                      print_commands=True,
                      print_tokens=True,
                      print_trees=True,
                      print_symbols=True):
    if print_tokens:
        _dump_tokens(env)
    if print_trees:
        print_forest(env, log, label, print_results)
    if print_commands:
        _print_commands(env, env.commands, log)
    if print_symbols:
        _dump_symbols(env.symbols)


def _print_commands(env, commands, log=None, label=None):
    idx = 0
    for i in range(0, len(commands)):
        t = commands[i]
        if t is None:
            continue
        idx += 1
        line = env.get_line(t.token.location.line).strip()
        ll = f'({label})' if label is not None else ''
        _t_print(log, f'\ntree{idx}:{ll}  {line}')
        print_node(t)


def _dump_tokens(env):
    print('tokens:')
    env.tokens.printall()



