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

    def error(self, message, loc, exception=True):
        loc.offset -= 1
        error_text = f'Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if exception:
            raise SemtexException(error_text)

    def warning(self, message, loc):
        loc.offset -= 1
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.environment.strict:
            raise SemtexException(error_text)

    def runtime_error(self, message, loc):
        loc.offset -= 1
        error_text = f'Runtime Error: {message}.'
        self.report(error_text, loc)
        raise Exception(error_text)

    def runtime_warning(self, message, loc):
        loc.offset -= 1
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        raise Exception(error_text)

    def report(self, message, loc):
        carrot = f'\n\n{self.environment.lines[loc.line]}\n{"^".rjust(loc.offset)}\n' if loc.line < len(self.environment.lines) else ''
        text = f"{carrot}\nFOCAL: {message} at position: {loc.line + 1}:{loc.offset}"
#       text = f"\n{message} at position: {loc.line + 1}:{loc.offset}"
        print(text)


# helpers
def _t_print(f, message):
    print(message)
    if f is not None:
        f.write(f'{message}\n')
