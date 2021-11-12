from enum import IntEnum, unique, auto
from queue import SimpleQueue

from runtime import exceptions
from runtime.environment import Environment

from interpreter.interpreter import Interpreter, _interpreterVisitNodeMappings


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
}


@unique
class COMMAND(IntEnum):
    NONE = 0
    APPLY_OPTIONS = auto()
    SHOW_OPTIONS = auto()


_commandLookup = {
    'option': COMMAND.APPLY_OPTIONS,
    'options': COMMAND.SHOW_OPTIONS,
}


#
# The Command interpreter allows over-riding behavior from the Interpreter.  It shares the same stack.
#

class CommandInterpreter(Interpreter):

    def __init__(self, environment, mapping=None):
        m = dict(_interpreterVisitNodeMappings if mapping is None else mapping)
        m.update(_commandVisitNodeMappings)
        super().__init__(environment=environment, mapping=m)
        self.environment = environment
        self.interpreter = None
        self.keywords = environment.keywords
        self.globals = environment.globals
        self.stack = environment.stack
        self._verbose = True

    def execute(self, interp):
        self.interpreter = interp
        try:
            self.apply(self.environment.commands)
            self.interpreter.apply(self.environment.trees)
        except Exception as e:
            exceptions.runtime_error(f'{e}')

    def apply(self, commands):
        if commands is None:
            return None
        for c in commands:
            self.visit(c)
#            v = self.stack.pop()
#            ty = type(v).__name__
#            if getattr(v, 'value', False):
#                v = v.value
#            c.value = v
#            if self._verbose:
#                print(f'\nresult: {ty.lower()}({v})\n')
        print(f'stack depth: {self.stack.depth()}\n')
        return self.trees

    # default
    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        self._print_node(node)
        return node.value

    def process_command(self, node, label=None):
        self._print_node(node)
        self.indent()
        if node.expr is not None:
            self.visit(node.expr)
        cid = _cmd2id(node)
        if cid in _commandDispatch.keys():
            info = _commandDispatch[cid]
            argc = len(info[1])
            args = []
            while argc > 0:
                args.append(self.stack.pop())
                argc -= 1
            _dispatchCommand(cid, args)
        self.dedent()


# ---------------------
# command handlers
# ---------------------
def apply_options(node):
    d = node.to_dict(unbox_values=True)
    Environment.current.update_options(d)
    pass


def get_options():
    d = Environment.current.to_dict()
    _dump_dictionary(d, "options")


# helpers
def _cmd2id(node):
    if node.token.lexeme in _commandLookup.keys():
        cmd = _commandLookup[node.token.lexeme]
        return cmd
    else:
        raise Exception(f'Invalid command: {node.token.lexeme}')


def _dispatchCommand(cid, arg):
    if cid in _commandDispatch.keys():
        info = _commandDispatch[cid]
        fn = info[0]
        return fn(*arg)


def _dump_dictionary(d, label=None):
    if label is not None:
        print(f"\n\n{label}: ")
    idx = 0
    q = SimpleQueue()
    q.put(d)
    while not q.empty():
        s = q.get()
        for k in s.keys():
            v = s[k]
            if type(v).__name__ == 'Object':
                q.put(v)
            print(f'{idx:5d}:  `{k}` = {v}')
            idx += 1


_commandDispatch = {
    COMMAND.APPLY_OPTIONS: (apply_options, ':'),
    COMMAND.SHOW_OPTIONS: (get_options, ''),
}
