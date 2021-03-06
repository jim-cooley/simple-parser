#
# this file contains toke tree rewriters used by the Parser and others
#
from abc import ABC

from runtime.tree import FnRef, Ref
from interpreter.modifytree import TreeModifier
from interpreter.visitor import BINARY_NODE, UNARY_NODE, SEQUENCE_NODE, TRINARY_NODE

_rewriteBaseNodeTypeMapping = {
    'ApplyChainProd': BINARY_NODE,
    'Assign': BINARY_NODE,
    'BinOp': BINARY_NODE,
    'Block': SEQUENCE_NODE,
    'Dataset': SEQUENCE_NODE,
    'Dict': SEQUENCE_NODE,
    'Define': BINARY_NODE,
    'DefineChainProd': BINARY_NODE,
    'DefineFn': BINARY_NODE,
    'DefineVal': BINARY_NODE,
    'DefineVar': BINARY_NODE,
    'DefineValFn': BINARY_NODE,
    'DefineVarFn': BINARY_NODE,
    'FnCall': BINARY_NODE,
    'FnRef': BINARY_NODE,
    'Flow': SEQUENCE_NODE,
    'Generate': SEQUENCE_NODE,
    'GenerateRange': SEQUENCE_NODE,
    'Index': BINARY_NODE,
    'IndexSet': TRINARY_NODE,
    'IfThenElse': TRINARY_NODE,
    'List': SEQUENCE_NODE,
    'NamedTuple': SEQUENCE_NODE,
    'PropCall': BINARY_NODE,
    'PropRef': BINARY_NODE,
    'PropSet': TRINARY_NODE,
    'Series': SEQUENCE_NODE,
    'Set': SEQUENCE_NODE,
    'Slice': TRINARY_NODE,
    'Tuple': SEQUENCE_NODE,
    'UnaryOp': UNARY_NODE,
}

_rewriteGetsNodeTypeMapping = {
    'Get': 'rewrite_get',
}

_rewriteFnCallNodeTypeMapping = {
    'FnCall': 'rewrite_fncall',
}


class BaseRewriter(TreeModifier, ABC):
    def __init__(self, mapping=None, apply_parent_fixups=True):
        if mapping is None:
            mapping = _rewriteBaseNodeTypeMapping
        super().__init__(mapping=mapping, apply_parent_fixups=apply_parent_fixups)

    def apply(self, root):
        root = self.visit(root)
        return root

    def visit_node(self, node, label=None):
        super().visit_node(node, label)
        return node


class RewriteGets2Refs(BaseRewriter, ABC):
    def __init__(self, mapping=None, apply_parent_fixups=True):
        m = dict(_rewriteBaseNodeTypeMapping if mapping is None else mapping)
        m.update(_rewriteGetsNodeTypeMapping)
        super().__init__(mapping=m, apply_parent_fixups=apply_parent_fixups)

    def rewrite_get(self, node, label=None):
        ref = node.to_ref()
        return ref


# turns FnCalls and Gets in LHS into FnDefs and Ref's
class RewriteFnCall2FnDef(RewriteGets2Refs, ABC):
    def __init__(self, mapping=None, apply_parent_fixups=True):
        m = dict(_rewriteBaseNodeTypeMapping if mapping is None else mapping)
        m.update(_rewriteFnCallNodeTypeMapping)
        super().__init__(mapping=m, apply_parent_fixups=apply_parent_fixups)

    def rewrite_fncall(self, node, label=None):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        assert isinstance(node.left, Ref), "node.left is not a Reference"
        n = FnRef(ref=node.left, op=node.token, parameters=node.right)
        node.left.parent = n
        node.right.parent = n
        return n


# turns FnCalls and Gets in LHS into DefineFns and Ref's
class RewriteFnCall2DefineFn(RewriteGets2Refs, ABC):
    def __init__(self, mapping=None, apply_parent_fixups=True):
        m = dict(_rewriteBaseNodeTypeMapping if mapping is None else mapping)
        m.update(_rewriteFnCallNodeTypeMapping)
        super().__init__(mapping=m, apply_parent_fixups=apply_parent_fixups)

    def rewrite_fncall(self, node, label=None):
        assert node.left is not None, "Invalid node passed to rewrite_fncall. node.left is None"
        node.left = self.visit(node.left)
        if node.right is not None:
            node.right = self.visit(node.right)
        assert isinstance(node.left, Ref), "node.left is not a Reference"
        n = FnRef(ref=node.left, op=node.token, parameters=node.right)
        node.left.parent = n
        if node.right is not None:
            node.right.parent = n
        return n
