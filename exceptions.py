# parsing and semantic analysis exception handling and helper functions

from indexed_dict import IndexedDict


class SemtexException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def getErrorFacility(name, options=None, env=None):
    if name not in _facilities.keys():
        f = ExceptionReporter(env=env, options=options)
        _facilities[name] = f
    return _facilities[name]


def runtime_error(message, loc=None):
    f = getErrorFacility('semtex')
    f.runtime_error(message, loc)


# strict warning becomes error if option.strict is true (variable used before being declared)
def runtime_strict_warning(message, loc=None):
    f = getErrorFacility('semtex')
    f.runtime_strict_warning(message, loc)


def runtime_warning(message, loc=None):
    f = getErrorFacility('semtex')
    f.runtime_warning(message, loc)


def setErrorConfiguration(name, options, env=None):
    f = getErrorFacility(name, options, env)
    f.set_options(options)
    f.environment = f.environment if env is None else env


class ExceptionReporter:

    def __init__(self, env=None, options=None):
        self.environment = env
        self.option = IndexedDict(items=options, defaults=_defaultOptions)

    def set_options(self, options):
        self.option.update(options)

    # error reporting
    def expected(self, expected, found):
        message = f'Expected {expected}, found {found.id.name}'
        self.error(message, found.location)

    def error(self, message, loc=None, exception=True):
        error_text = f'Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if exception:
            raise SemtexException(error_text)

    def strict_warning(self, message, loc=None):
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.option.strict or self.option.force_errors:
            raise SemtexException(error_text)

    def warning(self, message, loc=None):
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.option.force_errors:
            raise SemtexException(error_text)

    def runtime_error(self, message, loc=None):
        error_text = f'Runtime Error: {message}.'
        self.report(error_text, loc)
        raise SemtexException(error_text)

    def runtime_strict_warning(self, message, loc=None):
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        if self.option.strict or self.option.force_errors:
            raise SemtexException(error_text)

    def runtime_warning(self, message, loc=None):
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        if self.option.force_errors:
            raise SemtexException(error_text)

    def report(self, message, loc=None):
        if loc is not None:
            loc.offset -= 1
            carrot = ''
            if self.environment is not None:
                carrot = f'\n\n{self.environment.lines[loc.line]}\n{"^".rjust(loc.offset)}\n' if loc.line < len(self.environment.lines) else ''
            text = f"\n{carrot}\nFOCAL: {message} at position: {loc.line + 1}:{loc.offset}\n"
        else:
            text = f"FOCAL: {message}."
        print(text)


_defaultOptions = {
    'strict': False,
    'force_errors': False,
}

_facilities = {}
