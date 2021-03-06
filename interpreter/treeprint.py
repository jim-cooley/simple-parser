from runtime.literals import Literal, Str
from runtime.scope import Block, Flow
from runtime.tree import Ref, UnaryOp, PropRef, BinOp, FnCall, Generate, Assign, DefineFn, ApplyChainProd, Slice

from interpreter.notation import FunctionalNotationPrinter
from interpreter.visitor import NodeVisitor, BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, DEFAULT_NODE, VALUE_NODE, NATIVE_VALUE, \
    ASSIGNMENT_NODE, TRINARY_NODE

_nodeTypeMappings = {
    'Apply': ASSIGNMENT_NODE,
    'ApplyChainProd': ASSIGNMENT_NODE,
    'Assign': ASSIGNMENT_NODE,
    'BinOp': BINARY_NODE,
    'Block': SEQUENCE_NODE,
    'Bool': VALUE_NODE,
    'Combine': ASSIGNMENT_NODE,
    'Command': UNARY_NODE,
    'Dataset': SEQUENCE_NODE,
    'DateDiff': VALUE_NODE,
    'DateTime': VALUE_NODE,
    'Define': ASSIGNMENT_NODE,
    'DefineChainProd': ASSIGNMENT_NODE,
    'DefineFn': TRINARY_NODE,
    'DefineVal': ASSIGNMENT_NODE,
    'DefineVar': ASSIGNMENT_NODE,
    'DefineValFn': TRINARY_NODE,
    'DefineVarFn': TRINARY_NODE,
    'Dict': SEQUENCE_NODE,
    'Duration': VALUE_NODE,
    'Float': VALUE_NODE,
    'Flow': SEQUENCE_NODE,
    'FnCall': BINARY_NODE,
    'FnRef': BINARY_NODE,
    'Generate': SEQUENCE_NODE,
    'GenerateRange': SEQUENCE_NODE,
    'Get': VALUE_NODE,
    'Ident': VALUE_NODE,
    'IfThenElse': TRINARY_NODE,
    'Index': BINARY_NODE,
    'IndexSet': TRINARY_NODE,
    'Int': VALUE_NODE,
    'List': SEQUENCE_NODE,
    'Literal': VALUE_NODE,
    'NamedTuple': SEQUENCE_NODE,
    'Node': DEFAULT_NODE,
    'Percent': VALUE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'PropSet': TRINARY_NODE,
    'Ref': VALUE_NODE,
    'Return': UNARY_NODE,
    'Series': SEQUENCE_NODE,
    'Set': SEQUENCE_NODE,
    'Slice': TRINARY_NODE,
    'Str': VALUE_NODE,
    'Time': VALUE_NODE,
    'Tuple': SEQUENCE_NODE,
    'UnaryOp': UNARY_NODE,
    'int': NATIVE_VALUE,
    'str': NATIVE_VALUE,
}


class TreePrint(NodeVisitor):
    def __init__(self):
        super().__init__(_nodeTypeMappings)
        self._ncount = 1
        self._body = []
        self._depth = 0

    def indent(self):
        self._depth += 1

    def dedent(self):
        self._depth -= 1

    def apply(self, tree=None):
        self.visit(tree)
        return self._body

    def format_indent(self):
        return '' if self._depth < 1 else ' '.ljust(self._depth * 4)

    def visit_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1

    # helpers
    def visit_intrinsic(self, value, label=None):
        self._print_object(value, label)
        self._ncount += 1

    def visit_tuple(self, node, label=None):
        self._visit_sequence(node)

    def visit_assignment_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_binary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_sequence(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        if node.items() is not None:
            self._visit_sequence(node.items())

    def _visit_sequence(self, li, label=None):
        self.indent()
        if len(li) != 0:
            for n in li:
                if n is not None:
                    self.visit(n)
        self.dedent()

    def visit_trinary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        if hasattr(node, 'args'):
            self.visit(node.args)
        else:
            self.visit(node.middle)
        self.dedent()

    def visit_unary_node(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.expr)
        self.dedent()

    def visit_value(self, node, label=None):
        self._print_node(node, label)
        node._num = self._ncount
        self._ncount += 1

    def _print_object(self, obj, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
        line = '{:5d} : {}{} {}'.format(self._ncount, indent, label, obj)
        self._body.append(line)

    def _print_node(self, node, label=None):
        indent = '' if self._depth < 1 else ' '.ljust(self._depth * 4)
#       op = f' {_._tk2glyph[node.op]}' if isinstance(node, Assign) or isinstance(node, BinOp) else ''
#       op = f' TK.{node.op.name}' if isinstance(node, Assign) else ''
        op = ''
        line = f'{self._ncount:5d}  : {indent}{_format_node(node)}'
        self._body.append(line)


def print_forest(env, logger=None, label=None, print_notation=True, print_results=True):
    idx = 0
    trees = env.trees
    for i in range(0, len(trees)):
        t = trees[i]
        if t is None or t.root is None:
            continue
        idx += 1
        line = env.get_line(t.root.token.location.line).strip()
        ll = f'({label})' if label is not None else ''
        logger.print(f'\ntree{idx}:{ll}  {line}')
        print_tree(t, logger=logger, label=label, print_notation=print_notation, print_results=print_results)


def print_tree(tree, logger=None, label=None, print_notation=True, print_results=True):
    printer = FunctionalNotationPrinter()
    if tree is None or tree.root is None:
        return
    if print_notation:
        print(f'notation: {printer.apply(tree.root)}')
    if tree.values is not None and print_results:
        v = tree.values if type(tree.values).__name__ != 'list' else tree.values[0]
        if v is not None:
            if hasattr(v, 'value'):
                v = v.value
            ty = type(v).__name__
            if v is None:
                ty = 'Lit'
            if print_results:
                logger.print(f'result: {ty}({v})')
    print_node(tree.root, logger=logger, print_notation=False)


def print_node(node, logger=None, label=None, print_notation=True):
    printer = FunctionalNotationPrinter()
    if node is None:
        return
    if print_notation:
        print(f'notation: {printer.apply(node)}')
    dt = TreePrint()
    viz = dt.apply(node)
    for tree in viz:
        logger.print(tree)


def print_results(env, logger=None):
    idx = 0
    trees = env.trees
    for i in range(0, len(trees)):
        t = trees[i]
        if t is None or t.root is None:
            continue
        idx += 1
        logger.print(f'\ntree{idx}:')
        if t.values is not None and print_results:
            v = t.values if type(t.values).__name__ != 'list' else t.values[0]
            if v is not None:
                if hasattr(v, 'value'):
                    v = v.value
                ty = type(v).__name__
                if v is None:
                    ty = 'Lit'
                if print_results:
                    logger.print(f'result: {ty}({v})')


def _format_token(tk, print_value=True):
    _tname = f'.{tk.id.name}(' if hasattr(tk.id, "name") else f'({tk.id}, '
    _tclass = f'{tk.t_class.name}' if hasattr(tk.t_class, "name") else 'TCL({tk.t_type})'
    _tvalue = 'None' if tk.value is None else f'{tk.value}'
    _tlexeme = f'\'{tk.lexeme}\'' if tk.lexeme is not None else 'None'
    #    _tloc = f'line:{tk.location.line + 1}, pos:{tk.location.offset - 1}'
    if _tlexeme == '\'\n\'':
        _tlexeme = "'\\n'"
    if print_value:
        text = f'TK{_tname}({_tclass}, {_tlexeme}, v={_tvalue})'
    else:
        text = f'TK{_tname}({_tclass}, {_tlexeme})'
    return text


def _format_node(node, print_location=False):
    ty = type(node).__name__
    v = node.value
    lex = node.token.lexeme
    tk = node.token.id
    loc = f'{_format_loc(node.token.location)}' if print_location else ''
    text = None
    lbc, rbc = '{', '}'
    if isinstance(node, ApplyChainProd):
        return f'{_format_binary_node(node, node.right, node.left, lex)}{loc}'
    if isinstance(node, DefineFn):
        return f'{_format_binary_node(node, node.left, node.right, lex)}{loc}'
    elif isinstance(node, Assign):
        return f'{_format_binary_node(node, node.left, node.right, lex)}{loc}'
    elif isinstance(node, Flow):
        return f'{ty}{lbc}TK.{tk.name}, \'{lex}\' len={len(node)}{rbc}{loc}'
    elif isinstance(node, Block):
        return f'{ty}{lbc}TK.{tk.name}, len={len(node)}{rbc}{loc}'
    elif isinstance(node, Slice):
        return f'{_format_slice(node)}{loc}'
    elif isinstance(node, FnCall):
        return f'{ty}(\'{node.left.token.lexeme}\'){loc}'
    elif isinstance(node, Generate):
        return f'{ty}(TK.{node.target.name}, len={len(node.items())}){loc}'
    elif isinstance(node, PropRef):
        return f'{_format_binary_node(node, node.left, node.right, lex)}{loc}'
    elif isinstance(node, Ref):
        return f'{ty}(TK.{tk.name}, \'{lex}\'){loc}'
    elif isinstance(node, BinOp):
        op = node.op
        return f'{ty}(TK.{op.name}, \'{lex}\'){loc}'
    elif isinstance(node, UnaryOp):
        op = node.op
        return f'{ty}(TK.{op.name}, \'{lex}\'){loc}'
    elif isinstance(node, Str):
        return f'{ty}(TK.{tk.name}, \'{node.value}\'){loc}'
    elif isinstance(node, Literal):
        return f'{ty}(TK.{tk.name}, {node.value}){loc}'
    elif hasattr(node, 'op'):
        op = node.op
        return f'{ty}(TK.{op.name}, TK.{tk.name}, \'{lex}\'){loc}'
    else:
        return f'{ty}(TK.{tk.name}, v={node.value}, \'{lex}\'){loc}'


def _format_slice(node):
    ty = type(node).__name__
    start = node.start
    end = node.end
    step = node.step
    lval = "None"
    rval = "None"
    sval = "1"
    if start is None:
        lval = ''
    elif isinstance(start, Literal):
        lval = f'{start}'
    else:
        lty = type(start).__name__
        ltk = start.token
        lval = f'{lty}(TK.{ltk.id.name}, \'{start.lexeme}\')'
    if end is None:
        rval = ''
    elif isinstance(end, Literal):
        rval = f'{end}'
    else:
        rty = type(start).__name__
        rtk = end.token
        rval = f'{rty}(TK.{rtk.id.name}, \'{end.lexeme}\')'
    if step is None:
        sval = ''
    elif isinstance(step, Literal):
        sval = f'{step}'
    else:
        sty = type(start).__name__
        stk = step.token
        sval = f'{sty}(TK.{stk.id.name}, \'{step.lexeme}\')'
    return f'Slice({lval} : {rval} :: {sval})'


def _format_binary_node(node, left, right, lex):
    ty = type(node).__name__
    lval = f'{left}'
    if hasattr(left, 'name'):
        lval = f'{left.name}'
    if right is not None:
        if isinstance(right, Literal):
            r = f'{right}'
        else:
            rty = type(right).__name__
            rtk = right.token
            r = f'{rty}(TK.{rtk.id.name}, \'{right.lexeme}\')'
    else:
        r = 'TK.NONE'
    return f'{ty}(TK.{node.op.name}: {lval} {lex} {r})'


def _format_loc(loc):
    if loc is None:
        return ''
    return f': line:{loc.line}, pos:{loc.offset}'


def fn_foo():
    if isinstance(node.right, Literal):
        r = f'{node.right}'
    else:
        rty = type(node.right).__name__
        rtk = node.right.token
        r = f'{rty}()'
    return f'{ty}(TK.{node.op.name}: {node.left.name}({node.args}) = {r}){loc}'
