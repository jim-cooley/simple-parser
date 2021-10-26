import os
import traceback
from abc import abstractmethod, ABC

from notation import NotationPrinter
from treedump import DumpTree

_LOG_DIRECTORY = "./etc/test/log"
_SCRIPT_SEARCH_PATH = [
    ".",
    "./test/cases",
    "./etc/test",
    "../etc/test",
]


class TestSuiteRunner(ABC):

    def __init__(self, test_data, skip_tests=None, prefix='', log_dir=None):
        self.tests = test_data
        self.skip_tests = skip_tests if skip_tests is not None else []
        self.prefix = prefix
        self.interactive = False
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
            self._generate_empty_log(name, name, f'invalid test suite: {name}, skipping.\n\n')
            return
        print(f'\n\nsuite: {name}')
        cases = self.tests[name]
        idx = 0
        if type(cases).__name__ == "list":
            for test in cases:
                idx += 1
                self._run_single_test(name, test, idx)
            return
        else:
            fname = _find_test_file(name, _SCRIPT_SEARCH_PATH)
            tt = os.path.splitext(fname)[1]
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
        label = f'test: "{test}"' if idx is None else f'test: {idx}: "{test}"'
        fname = f'{self.logs_dir}/{self.prefix}{fn}'
        with open(fname, 'w') as log:
            _t_print(log, f'\n\n{label}')
            if not self.interactive:
                self.run_protected_test(log, name, test)
            else:
                self.run_unprotected_test(log, name, test)

    def _generate_empty_log(self, name, test, message='', idx=None):
        fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
        label = f'test: "{test}"' if idx is None else f'test: {idx}: "{test}"'
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
    raise IOError(f'invalid test suite: {name}, is not a test file')


def _log_exception(e, log, name):
    trace = traceback.format_exc()
    _t_print(log, f'FAIL: \'{name}\' failed with Exception {e}\n')
    if trace is not None:
        print(f'{trace}')


def _dump_environment(env, log=None, label=None):
    _dump_tokens(env)
    _dump_trees(env, log, label)
    _dump_commands(env, log)


def _dump_commands(env, log=None, label=None):
    printer = NotationPrinter()
    idx = 0
    for i in range(0, len(env.commands)):
        t = env.commands[i]
        if t is None:
            continue
        idx += 1
        line = _get_line(t.token.location, env.lines).strip()
        ll = f'({label})' if label is not None else ''
        _t_print(log, f'\ntree{idx}:{ll}  {line}')
        print(f'notation: {printer.apply(t)}')
        dt = DumpTree()
        viz = dt.apply(t)
        for v in viz:
            _t_print(log, v)


def _dump_tokens(env):
    print('tokens:')
    env.tokens.printall()


def _dump_trees(env, log=None, label=None):
    printer = NotationPrinter()
    idx = 0
    trees = env.trees
    for i in range(0, len(trees)):
        t = trees[i]
        if t is None:
            continue
        idx += 1
        line = _get_line(t.root.token.location, env.lines).strip()
        ll = f'({label})' if label is not None else ''
        _t_print(log, f'\ntree{idx}:{ll}  {line}')
        print(f'notation: {printer.apply(t.root)}')
        if t.values is not None:
            v = t.values if type(t.values).__name__ != 'list' else t.values[0]
            ty = type(v).__name__
            if getattr(v, 'value', False):
                v = v.value
            if v is None:
                ty = 'Lit'
            _t_print(log, f'result: {ty}({v})')
        else:
            _t_print(log, f'result: None')
        dt = DumpTree()
        viz = dt.apply(t.root)
        for v in viz:
            _t_print(log, v)


# helpers
def _get_line(loc, lines):
    if loc.line < len(lines):
        return lines[loc.line]
    return ''


def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')
