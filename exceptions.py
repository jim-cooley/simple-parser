# parsing and semantic analysis exception handling and helper functions
from environment import Environment


def _contains(values, tkid):
    if values is None:
        return False
    for n in values:
        if n is None:
            continue
        if n.token.id == tkid:
            return True
    return False


def _contains_set(values, tk_list):
    if values is None:
        return False
    for n in values:
        if n is None:
            continue
        if n.token.id in tk_list:
            return True
    return False


def _contains_cl_set(values, tcl_list):
    if values is None:
        return False
    for n in values:
        if n is None:
            continue
        if n.token.t_class in tcl_list:
            return True
    return False


def _expect(node, ex_tid):
    if node.token.id != ex_tid:
        _expected(expected=f'{ex_tid.name}', found=node.token)
    return node


def _expect_cl(node, ex_tcl):
    if node.token.t_class != ex_tcl:
        _expected(expected=f'{ex_tcl.name}', found=node.token)
    return node


def _expect_in_cl(node, tcl_list):
    if node.token.t_class not in tcl_list:
        _expected(expected=f'{tcl_list}', found=node.token)
    return node


def _match_set(node, tk_list):
    return node is not None and node.token.id in tk_list


def _match_cl_set(node, tcl_list):
    return node is not None and node.token.t_class in tcl_list


# error reporting
def _expected(expected, found):
    token = found
    message = f'Expected {expected}, found {token.id.name}'
    _error(message, token.location)


def _error(message, loc):
    loc.offset -= 1
    error_text = f'Invalid Syntax: {message}.'
    _report(error_text, loc)
    raise Exception(error_text)


def _warning(message, loc):
    loc.offset -= 1
    error_text = f'Warning: Invalid Syntax: {message}.'
    _report(error_text, loc)
    if Environment.current.strict:
        raise Exception(error_text)


def _runtime_error(message, loc):
    loc.offset -= 1
    error_text = f'Runtime Error: {message}.'
    _report(error_text, loc)
    raise Exception(error_text)


def _runtime_warning(message, loc):
    loc.offset -= 1
    error_text = f'Warning: {message}.'
    _report(error_text, loc)
    raise Exception(error_text)


def _report(message, loc):
# carrot = f'\n\n{self._parse_string}\n{"^".rjust(loc.offset)}\n'
# text = f"{carrot}\n{message} at position: {loc.line + 1}:{loc.offset}"
    text = f"\n{message} at position: {loc.line + 1}:{loc.offset}"
    print(text)
