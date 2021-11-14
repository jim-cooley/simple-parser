from enum import IntEnum, unique, auto
from queue import SimpleQueue

from interpreter.notation import FunctionalNotationPrinter
from interpreter.treeprint import print_forest
from runtime import exceptions
from runtime.dataframe import Dataset
from runtime.environment import Environment
from runtime.options import getOptions
from runtime.print import print_dataframe, _t_print
from interpreter.interpreter import Interpreter, _interpreterVisitNodeMappings
from runtime.exceptions import getLogFacility
from runtime.runtime import load_script
from runtime.scope import Scope
from runtime.tree import AST

_VISIT_ASSIGNMENT = 'visit_assignment'
_VISIT_DEFINITION = 'visit_definition'
_VISIT_IDENT = 'visit_ident'
_VISIT_LITERAL = 'visit_literal'
_VISiT_LEAF = 'visit_value'

_PROCESS_APPLY = 'process_apply'
_PROCESS_BINOP = 'process_binop'
_PROCESS_BLOCK = 'process_block'
_PROCESS_FLOW = 'process_flow'
_PROCESS_GET = 'process_get'
_PROCESS_PROPREF = 'process_propref'
_PROCESS_REF = 'process_ref'
_PROCESS_SEQUENCE = 'process_sequence_node'
_PROCESS_UNOP = 'process_unop'

_NATIVE_LIST = 'visit_list'
_NATIVE_VALUE = 'process_intrinsic'

_commandVisitNodeMappings = {
    'Command': 'process_command',
    'Get': 'process_get',
    'Ref': 'process_ref',
}


@unique
class SLOT(IntEnum):
    INVOKE = 0
    INIT = 1
    ARGC = 2
    HELP = 3


#
# The Command interpreter allows over-riding behavior from the Interpreter.  It shares the same stack.
#

class CommandShell(Interpreter):

    def __init__(self, interpreter=None, mapping=None):
        m = dict(_interpreterVisitNodeMappings if mapping is None else mapping)
        m.update(_commandVisitNodeMappings)
        super().__init__(mapping=m)
        self.options = getOptions('focal')
        self.stack = None  # environment.stack
        self.environment = None
        self.interpreter = interpreter
        self._verbose = True

    def execute(self, environment, interpreter):
        try:
            self.environment = environment
            self.stack = environment.stack
            self.apply(environment)  # execute commands
            if not self.options.no_run:
                interpreter.apply(environment)  # execute script
        except Exception as e:
            if self.options.throw_errors:
                exceptions.runtime_error(f'{e}')
            else:
                exceptions.runtime_warning(f'{e}')

    def apply(self, environment=None):
        if environment.commands is None:
            return None
        for c in environment.commands:
            self.visit(c)
        return environment

    # default
    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        return node.value

    # Get
    def process_get(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_ref(ref=node))

    # Ref
    def process_ref(self, node, label=None):
        self._print_node(node)
        self.stack.push(reduce_ref(ref=node))

    # PropRef
    def process_propref(self, node, label=None):
        self._print_node(node)
        self.visit(node.left)
        left = self.stack.pop()
        if isinstance(left, Scope):
            Environment.enter(left)
        self.visit(node.right)
        if isinstance(left, Scope):
            Environment.leave()
        right = self.stack.pop()
        self.stack.push(reduce_propref(left, right))

    # Command
    def process_command(self, node, label=None):
        self._print_node(node)
        self.indent()
        if node.expr is not None:
            self.visit(node.expr)
        _dispatchCommand(self.environment, node.token.lexeme, _command_funcdesc, _command_aliases)
        self.dedent()


# ---------------------
# evaluate over-rides
# ---------------------
def reduce_ref(scope=None, ref=None):
    scope = Environment.current.scope if scope is None else scope
    symbol = None if not isinstance(ref, AST) else scope.find(token=ref.token)
    if symbol is None:
        if hasattr(ref, 'name'):
            return ref.name
        return ref
    return symbol


def reduce_propref(left=None, right=None):
    scope = Environment.current.scope
    symbol = None if not isinstance(left, AST) else scope.find(token=left.token)
    if symbol is None:
        if hasattr(left, 'name'):
            left = left.name
        if hasattr(right, 'name'):
            right = right.name
        name = f'{left}.{right}'
        return name
    if isinstance(left, Scope):
        return reduce_ref(left, right)
    return f'{left.name}.{right.name}'


# ---------------------
# dispatch
# ---------------------
def _dispatchCommand(env, cmd, disptab, aliases):
    if cmd in aliases:
        cmd = aliases[cmd]
    if cmd in disptab:
        fndesc = disptab[cmd]
        fn = fndesc[SLOT.INVOKE]
        argc = len(fndesc[SLOT.ARGC])
        if argc > 0:
            args = []
            while argc > 0:
                if env.stack.depth() > 0:
                    args.append(env.stack.pop())
                argc -= 1
            return fn(env, args)
        else:
            return fn(env)


# ---------------------
# base commands
# ---------------------

def do_break(env):
    breakpoint()


def do_help(env, cmd):
    if cmd is not None:
        cmd = cmd[0]
    cmd = 'commands' if (cmd is None or len(cmd) < 1) else cmd
    if cmd not in _funcdesc_locator:
        cmd = 'commands'
    print("\n\n")
    _print_help_text('help')
    _print_commands(_funcdesc_locator[cmd], label=f'{cmd}:')


def do_load_script(env, args):
    fname = args[0]
    source = load_script(fname)
    env.set_source(source)
    show_sourcelines(env)


def do_parse(env):
    source = env.source
    env.parser.parse(source=source)
    show_tokens(env)


def do_run(env):
    pass


def set_options(env, args):
    option = args[0]
    d = {option.name: option.value}
    Environment.current.update_options(d)
    pass


def show_options(env):
    d = env.options.to_dict()
    _print_dictionary(d, label="options", skip=['_defaults'])


# ---------------------
# print
# ---------------------
def do_print(env, vargs):
    logger = getLogFacility('focal')
    line = []
    for i in range(0, len(vargs)):
        o = vargs[i]
        if isinstance(o, Dataset):
            print_dataframe(o)
        else:
            if hasattr(o, 'format'):
                text = o.format()
            else:
                text = f'{o}'
            line.append(text)
    text = ' '.join(line)
    _t_print(logger, text)
    return vargs.message


# ---------------------
# show
# ---------------------
def do_show(env, args):
    cmd = args[0]
    _dispatchCommand(env, cmd, _show_funcdesc, _show_aliases)


def show_aliases(env):
    _print_dictionary(_command_aliases, 'commands:')
    _print_dictionary(_show_aliases, 'show:')


def show_commands(env):
    _print_commands(_command_funcdesc, 'commands:')
    _print_commands(_show_funcdesc, 'show:')


def show_notation(env):
    printer = FunctionalNotationPrinter(indent=True)
    trees = env.trees
    if trees is None or len(trees) < 1:
        return
    idx = 0
    for i in range(0, len(trees)):
        idx += 1
        t = trees[i]
        print(f'\ntree{idx}:')
        if t.root is None:
            print("<empty>")
            continue
        print(f'{printer.apply(t.root)}')


def show_stack(env):
    stack = env.stack
    _print_stack(env.stack, label="stack")


def stack_depth(env):
    print(f'stack depth: {env.stack.depth()}')


def show_tokens(env):
    print('tokens:')
    if env.tokens is not None:
        env.tokens.printall()
    else:
        print("None")


def show_tree(env):
    _print_banner("parse tree")
    print_forest(env, env.logger, label=None, print_results=env.options.verbose, print_notation=False)


def show_sourcelines(env):
    _print_lines(env.lines, "source")


# ---------------------
# helpers
# ---------------------
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


def _print_commands(table, label=None):
    if label is not None:
        print(f"\n{label}: ")
    idx = 0
    for cmd in table:
        fndesc = table[cmd]
        print(f'{idx:5d}:  `{cmd}`: {fndesc[SLOT.HELP]}')
        idx += 1


def _print_dictionary(d, label=None, skip=None, stringify=False):
    if label is not None:
        print(f"\n{label}: ")
    idx = 0
    skip = skip or []
    q = SimpleQueue()
    q.put(d)
    while not q.empty():
        s = q.get()
        for k in s:
            if k not in skip:
                v = s[k]
                if type(v).__name__ == 'Object':
                    q.put(v)
                if stringify:
                    if hasattr(v, 'name'):
                        v = v.name
                    v = f'{v}'
                print(f'{idx:5d}:  `{k}` = {v}')
                idx += 1


def _print_help_text(key):
    key = 'help' if key is None else key
    key = 'help' if key not in _help_text else key
    _print_lines(_help_text[key], numbered=False)


def _print_stack(stack, label=None):
    if label is not None:
        print(f"\n{label}: ")
    print(f'stack depth: {stack.depth()}')
    if not stack.is_empty():
        idx = 1
        while idx <= stack.depth():
            item = stack.peek(-idx)
            print(f'{idx:5d}:  {item}')
            idx += 1


def _print_lines(lines, label=None, numbered=True):
    if label is not None:
        print(f"\n{label}: ")
    idx = 0
    for line in lines:
        if numbered:
            print(f'{idx:5d}:  {line.rstrip()}')
        else:
            print(f'{line.rstrip()}')
        idx += 1


# these are function descriptors for the intrinsic functions
# the format is (invoke_fn, init_fn)
_command_funcdesc = {
    'break': (do_break, None, '', 'break into the debugger'),
    'help': (do_help, None, ':', 'print help info on commands'),
    'load': (do_load_script, None, ':', 'load script file'),
    'options': (show_options, None, '', 'show options'),
    'parse': (do_parse, None, '', 'parse loaded script'),
    'print': (do_print, None, ':', 'print'),
    'run': (do_run, None, '', 'run interpreter'),
    'set': (set_options, None, ':', 'set options'),
    'show': (do_show, None, ':', 'show various things, see `help show`'),
    'show.stack': (do_show, None, ':', 'display the stack'),
}

_command_aliases = {
    'opt': 'options',
    'p': 'print',
    's': 'show',
}

_show_funcdesc = {
    # functions:
    'aliases': (show_aliases, None, '', 'list aliases for commands'),
    'options': (show_options, None, '', 'show options'),
    'notation': (show_notation, None, '', 'show the notation for commands before they are executed'),
    'source': (show_sourcelines, None, '', 'print out the current source'),
    'stack': (show_stack, None, '', 'show information related to the stack (see `help stack`, or `help show.stack`'),
    'stack_depth': (stack_depth, None, '', 'display stack depth'),
    'tokens': (show_tokens, None, '', 'display the tokens for the current source'),
    'tree': (show_tree, None, '', 'display the current parse tree(s)'),
}

_show_aliases = {
    'a': 'aliases',
    'n': 'notation',
    'o': 'options',
    'sd': 'stack_depth',
    'stack.depth': 'stack_depth',
}

_funcdesc_locator = {
    'commands': _command_funcdesc,
    'show': _show_funcdesc,
}

_help_text = {
    'help': ["Focal is a formulaic language and this is a console for it.",
             "To enter and run Focal language, simply enter your expression.  To invoke interpreter commands,",
             "use '%%' to prefix the commands, as is '%%help', or 'x = 5'.\n"]
}
