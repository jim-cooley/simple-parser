from conversion import c_node2float, c_node2int, c_node2bool
from exceptions import _runtime_error
from tokens import TK


def decrement_literal(node):
    tid = node.token.id
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        n = c_node2float(node)
        n.value -= 1
    else:
        n = c_node2int(node)
        n.value -= 1
    return n


def increment_literal(node):
    tid = node.token.id
    if tid in [TK.FLOT, TK.PCT, TK.DUR]:
        n = c_node2float(node)
        n.value += 1
    else:
        n = c_node2int(node)
        n.value += 1
    return n


def negate_literal(node):
    token = node.token
    tid = token.id
    if tid in [TK.INT, TK.FLOT, TK.PCT, TK.DUR]:
        node.value = - node.value
        return node
    elif tid in [TK.BOOL]:
        node.value = not node.value
        return node
    elif tid == TK.STR:
        try:
            v = - int(node.value)
            node.value = v
            node.token.id = TK.INT
            return node
        except ValueError as e:
            pass
    elif tid == TK.EMPTY:
        return node
    _runtime_error("Unsupported type for Unary minus", loc=token.location)


def not_literal(node):
    n = c_node2bool(node)
    n.value = not n.value
    return n