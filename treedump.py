import tokens as _
from tree import NodeVisitor


class DumpTree(NodeVisitor):
    def __init__(self):
        self._ncount = 1
        self._body = []
        self._indent_level = 0
        self._indent = ''

    def indent(self):
        self._indent_level += 1
        self._indent = ' '.ljust(self._indent_level * 4)
        return

    def dedent(self):
        self._indent_level -= 1
        self._indent = ' '.ljust(self._indent_level * 4)

    def visit_BinOp(self, node):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, 'BinOp',node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.left)
        self.visit(node.right)
        self.dedent()

    def visit_Bool(self, node):
        self.visit_value('Bool', node)

    def visit_Command(self, node):
        self.visit_unary_node('Command', node)

    def visit_DateDiff(self, node):
        self.visit_value('DateDiff', node)

    def visit_DateTime(self, node):
        self.visit_value('DateTime', node)

    def visit_Duration(self, node):
        self.visit_value('Dur', node)

    def visit_Float(self, node):
        self.visit_value('Float', node)

    def visit_FnCall(self, node):
        s = '{}node{}:{} {}]'.format(self._indent, self._ncount, 'FnCall', node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.parameter_list)
        self.dedent()

    def visit_Ident(self, node):
        self.visit_value('Ident', node)

    def visit_Int(self, node):
        self.visit_value('Int', node)

    def visit_Percent(self, node):
        self.visit_value('Percent', node)

    def visit_PropCall(self, node):
        s = '{}node{}:{} {}.{}]'.format(self._indent, self._ncount, 'PropCall', node.token.format(), node.member.value)
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.visit(node.parameter_list)

    def visit_PropRef(self, node):
        if type(node).__name__ == 'Ident':
            s = '{}node{}:{} [{}("{}.{}")]'.format(self._indent, self._ncount, 'PropRef', _.Token.format_tid(node.token), node.token.value, node.member.value)
        else:
            s = '{}node{}:{} [{}]'.format(self._indent, self._ncount, 'PropRef', node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.member)
        self.dedent()

    def visit_Seq(self, node):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, 'Seq', node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.visit_sequence(node.sequence)

    def visit_Set(self, node):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, 'Set', node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        if node.members is not None:
            self.visit_sequence(node.members.sequence)

    def visit_Str(self, node):
        self.visit_value('Str', node)

    def visit_Time(self, node):
        self.visit_value('Time', node)

    def visit_UnaryOp(self, node):
        self.visit_unary_node('UnaryOp', node)

# helpers
    def visit_sequence(self, slist):
        self.indent()
        if len(slist) != 0:
            for n in slist:
                if n is not None:
                    self.visit(n)
        self.dedent()

    def visit_value(self, label, node):
        s = '{}node:{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1

    def visit_unary_node(self, label, node):
        s = '{}node{}:{} {}'.format(self._indent, self._ncount, label, node.token.format())
        self._body.append(s)
        node._num = self._ncount
        self._ncount += 1
        self.indent()
        self.visit(node.expr)
        self.dedent()

    def dump(self, tree):
        self.visit(tree)
        return self._body
