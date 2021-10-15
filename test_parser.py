from etc.test.test_data import test_data, skip_tests
from parser import Parser
from treedump import DumpTree

# sma(20)       open.sma(20)
# (20) | sma    open | sma(20)
# {20} | sma    {open, 20} | sma
# name = 20     20 | name
# | send to
# >> project onto (**)
# u{,} - union
# n{,} - intersection
# s{}  - make into signal
# {} -> signal  {} | signal

_LOG_DIRECTORY = "./etc/log"
_test_suite = True       # False is useful for debugging, interactive.  True for test suites


def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')


def _run_single_test(name, test, idx=None):
    fname = f'{name}.log' if idx is None else f'{name}_{idx}.log'
    label = f'test: "{test}"' if idx is None else f'test: {idx}: "{test}"'
    with open(f'{_LOG_DIRECTORY}/{fname}', 'w') as log:
        _t_print(log, f'\n\n{label}')
        if _test_suite:
            _run_protected_test(log, name, test)
        else:
            _run_unprotected_test(log, name, test)


def _run_protected_test(log, name, test):
    try:
        parser = Parser(str=test)
        tree = parser.parse()
        _dump_tree(tree, log)
    except Exception as e:
        _t_print(log, f'FAIL: \'{name}\' failed with Exception {e}')


def _run_unprotected_test(log, name, test):
    parser = Parser(str=test)
    tree = parser.parse()
    _dump_tree(tree, log)


def _run_suite(name):
    if name not in test_data:
        print(f'invalid test suite: {name}')
    print(f'\n\nsuite: {name}')
    cases = test_data[name]
    idx = 0
    for test in cases:
        idx += 1
        _run_single_test(name, test, idx)


def _run_suites(suites):
    for name in suites:
        _run_suite(name)


def _run_full_pass():
    for suite in test_data.keys():
        if suite not in skip_tests:
            _run_suite(suite)


def test_language():
    #   lexer = Lexer(string="{ close >> sma(10) and close >> sma(20) } | buy( open.delay(1d) )")
    #   lexer = Lexer(string="{ close >| sma(10) and close <| sma(20) } ∩ open.delay(1d) | buy")
    #   lexer = Lexer(string="{ close >| sma(10) and close <| sma(20) } n open.delay(1d) | buy")
    #   lexer = Lexer(string="{ close >| sma(10) and close <| sma(20) } & open.delay(1d) | buy")
    #   lexer = Lexer(string="{ close >| sma(10) and close <| sma(20) } | sig * open.delay(1d) >> buy")
    #   lexer = Lexer(string="n{ close >| sma(10), close <| sma(20) } >> {open.delay(1d)} | buy")
    #   lexer = Lexer(string="{ close >| sma(10) and close <| sma(20) } | signal ** {open.delay(1d)} | buy")
    #   lexer = Lexer()
    #   parser = Parser(str="{ close >| sma(10) and close <| sma(20) } | signal >> {open.delay(1d)} | buy")
    #   parser = Parser(str="close >| sma(10) and close <| sma(20) | signal >> open.delay(1d) | buy")
    _run_suite('language')


def _dump_tree(tree, log=None):
    idx = 0
    for t in tree:
        idx += 1
        _t_print(log, f'\ntree{idx}:')
        dt = DumpTree()
        viz = dt.dump(t)
        for v in viz:
            _t_print(log, v)


# this is only for execution under debugger or via command-line
if __name__ == '__main__':

    # short-circuit
    _test_suite = True
    if not _test_suite:
        _run_suites([
            'duration',
        ])
    else:
        _run_full_pass()
