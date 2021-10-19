import os
import traceback
from abc import abstractmethod, ABC
from treedump import DumpTree

_LOG_DIRECTORY = "./etc/test/log"


class TestSuiteRunner(ABC):

    def __init__(self, test_data, skip_tests=None, prefix=''):
        self.tests = test_data
        self.skip_tests = skip_tests if skip_tests is not None else []
        self.prefix = prefix
        self.interactive = False

    @abstractmethod
    def run_unprotected_test(self, log, name, test):
        pass

    def run_protected_test(self, log, name, test):
        try:
            self.run_unprotected_test(log, name, test)
        except Exception as e:
            _log_exception(log, e, name)

    def run_suites(self, suites):
        for name in suites:
            self.run_suite(name)

    def run_full_pass(self):
        for suite in self.tests.keys():
            if suite not in self.skip_tests:
                self.run_suite(suite)

    def run_suite(self, name):
        if name not in self.tests:
            _generate_empty_log(name, name, f'invalid test suite: {name}, skipping.\n\n')
            return
        print(f'\n\nsuite: {name}')
        cases = self.tests[name]
        if type(cases).__name__ == "list":
            idx = 0
            for test in cases:
                idx += 1
                self._run_single_test(name, test, idx)
            return
        elif os.path.isfile(cases):
            fname = cases
        elif os.path.isfile(f'./etc/test/{cases}'):
            fname = f'./etc/test/{cases}'
        elif os.path.isfile(f'./etc/test/dsl/{cases}'):
            fname = f'./etc/test/dsl/{cases}'
        else:
            raise IOError(f'invalid test suite: {name}, is not a file')
        with open(fname, 'r') as file:
            test = file.read()
            self._run_single_test(name, test)

    def _run_single_test(self, name, test, idx=None):
        fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
        label = f'test: "{test}"' if idx is None else f'test: {idx}: "{test}"'
        with open(f'{_LOG_DIRECTORY}/{self.prefix}{fname}', 'w') as log:
            _t_print(log, f'\n\n{label}')
            if not self.interactive:
                self.run_protected_test(log, name, test)
            else:
                self.run_unprotected_test(log, name, test)


def _log_exception(e, log, name):
    trace = traceback.format_exc()
    _t_print(log, f'FAIL: \'{name}\' failed with Exception {e}\n')
    if trace is not None:
        print(f'{trace}')


def _dump_tree(tree, log=None):
    idx = 0
    for t in tree.nodes:
        idx += 1
        _t_print(log, f'\ntree{idx}:')
        dt = DumpTree()
        viz = dt.dump(t)
        for v in viz:
            _t_print(log, v)


# helpers
def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')


def _generate_empty_log(name, test, message='', idx=None):
    fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
    label = f'test: "{test}"' if idx is None else f'test: {idx}: "{test}"'
    with open(f'{_LOG_DIRECTORY}/{fname}', 'w') as log:
        _t_print(log, message)
