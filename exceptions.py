# parsing and semantic analysis exception handling and helper functions

class SemtexException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ExceptionReporter:

    def __init__(self, env):
        self.environment = env

    # error reporting
    def expected(self, expected, found):
        message = f'Expected {expected}, found {found.id.name}'
        self.error(message, found.location)

    def error(self, message, loc=None, exception=True):
        error_text = f'Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if exception:
            raise SemtexException(error_text)

    def warning(self, message, loc=None):
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.environment.strict:
            raise SemtexException(error_text)

    def runtime_error(self, message, loc=None):
        error_text = f'Runtime Error: {message}.'
        self.report(error_text, loc)
        raise Exception(error_text)

    def runtime_warning(self, message, loc=None):
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        raise Exception(error_text)

    def report(self, message, loc=None):
        if loc is not None:
            loc.offset -= 1
            carrot = f'\n\n{self.environment.lines[loc.line]}\n{"^".rjust(loc.offset)}\n' if loc.line < len(self.environment.lines) else ''
            text = f"{carrot}\nFOCAL: {message} at position: {loc.line + 1}:{loc.offset}"
        else:
            text = f"FOCAL: {message}."
        print(text)


# helpers
def runtime_warning(message, loc=None):
    error_text = f'Warning: {message}.'
    _report(error_text, loc)
    raise Exception(error_text)


def runtime_error(message, loc=None):
    error_text = f'Runtime Error: {message}.'
    _report(error_text, loc)
    raise Exception(error_text)


def _report(message, loc=None):
    if loc is not None:
        loc.offset -= 1
        text = f"FOCAL: {message} at position: {loc.line + 1}:{loc.offset}"
    else:
        text = f"FOCAL: {message}."
    print(text)


def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')
        f.flush()
    else:
        print('null file handle in _t_print')
