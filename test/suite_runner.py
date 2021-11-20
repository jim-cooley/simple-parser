import os
import traceback
from abc import abstractmethod, ABC
from multiprocessing import SimpleQueue

from runtime.environment import Environment
from interpreter.treeprint import print_forest, print_node
from runtime.exceptions import getLogFacility
from runtime.options import getOptions

_LOG_DIRECTORY = "./etc/test/log"
_SCRIPT_SEARCH_PATH = [
    ".",
    "./test/cases",
    "./etc/test",
    "../etc/test",
]

_option_defaults = {
    'strict': False,    # option_strict forces variables to be defined before they are used
    'force_errors': False,  # option_force_errors forces warnings into errors
    'throw_errors': True,
    'print_tokens': False,
    'no_run': False,
    'verbose': False,
    'log_filename': './focal.log'
}


class TestSuiteRunner(ABC):

    def __init__(self, test_data, skip_tests=None, prefix='', log_dir=None, env=None):
        self.tests = test_data
        self.skip_tests = skip_tests if skip_tests is not None else []
        self.prefix = prefix
        self.interactive = False
        self.environment = env
        self.logger = None
        self.options = None
        self.logs_dir = log_dir if log_dir is not None else _LOG_DIRECTORY

    @abstractmethod
    def run_unprotected_test(self, environment, name, test):
        pass

    def run_protected_test(self, log, name, test):
        try:
            self.logger = getLogFacility('focal', file=log)
            self.options = getOptions('focal', defaults=_option_defaults)
            self.environment = Environment()
            self.run_unprotected_test(self.environment, name, test)
            self.environment.close()
            self.environment = None
        except Exception as e:
            _log_exception(e, log, name)
            if self.environment is not None:
                self.environment.close()

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
        label = f'test:\n{test}' if idx is None else f'test: {idx}:\n{test}'
        fname = f'{self.logs_dir}/{self.prefix}{fn}'
        with open(fname, 'w') as log:
            _t_print(log, f'\n\n{label}')
            if not self.interactive:
                self.run_protected_test(log, name, test)
            else:
                self.run_unprotected_test(log, name, test)

    def _generate_empty_log(self, name, test, message='', idx=None):
        fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
        label = f'test:\n{test}' if idx is None else f'test: {idx}:\n{test}'
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


def _dump_environment(env, label=None, print_results=False, print_tokens=True, print_trees=True, print_symbols=False,
                      print_notation=True):
    logger = env.logger
    if print_tokens:
        _dump_tokens(env)
        logger.flush()
    if print_trees:
        _print_banner("parse tree")
        print_forest(env, logger, label, print_results=print_results, print_notation=print_notation)
        logger.flush()
    if print_symbols:
        _print_banner("symbols")
        _dump_keywords(logger, env.keywords)
        _dump_symbols(logger, env.scope)
        logger.flush()


def _print_commands(env, commands, logger=None, label=None):
    if len(commands) > 0:
        _print_banner("commands")
        idx = 0
        for i in range(0, len(commands)):
            t = commands[i]
            if t is None:
                continue
            idx += 1
            line = env.get_line(t.token.location.line).strip()
            ll = f'({label})' if label is not None else ''
            logger.print(f'\ntree{idx}:{ll}  {line}')
            print_node(t, logger=logger)


def _dump_tokens(env):
    print('tokens:')
    env.tokens.printall()


def _dump_symbols(logger, scope):
    logger.print("\n\nsymbols: ")
    idx = 0
    q = SimpleQueue()
    q.put(scope)
    while not q.empty():
        s = q.get()
        if s._members is None or len(s._members) == 0:
            continue
        if hasattr(s, 'token'):
            logger.print(f'\nscope: {s.token.lexeme}')
        else:
            logger.print(f'\nglobal scope:')
        for k in s._members.keys():
            v = s._members[k]
            if type(v).__name__ == 'Object':
                q.put(v)
                logger.print(f'{idx:5d}:  `{k}`: {v.qualname} : Object({v.token})')
                idx += 1


def _dump_keywords(logger, scope):
    if scope._members is None or len(scope._members) == 0:
        return
    print(f'\nkeywords:')
    idx = 0
    for k in scope._members.keys():
        v = scope._members[k]
        if type(v).__name__ == 'Token':
            print(f'{idx:5d}:  `{k}`: {v}')
            idx += 1


def _print_banner(label, width=None):
    width = width or 50
    print("\n")
    title = _expand_text(label.upper())
    _l = (width // 2) - len(title) // 2
    _l = max(_l, 0)
    print(f'# {"-" * width}')
    print(f'# {" ".ljust(_l)}{title}')
    print(f'# {"-" * width}')


def _expand_text(text):
    t = []
    for c in text:
        t.append(f'{c} ')
    return ''.join(t)


def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')
        f.flush()
