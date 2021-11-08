# parsing and semantic analysis exception handling and helper functions
import traceback
import warnings

from indexed_dict import IndexedDict
from logwriter import IndentedLogWriter


class SemtexError(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__(*args, **kwargs)


class SemtexWarning(Warning):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__(*args, **kwargs)


class SemtexRuntimeError(RuntimeError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__(*args, **kwargs)


class SemtexRuntimeWarning(RuntimeWarning):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__(*args, **kwargs)


def getErrorFacility(name, options=None, env=None, file=None):
    if name not in _facilities:
        f = ExceptionReporter(name, env=env, options=options, file=file)
        _facilities[name] = f
    return _facilities[name]


def removeErrorFacility(fac):
    if fac.name not in _facilities:
        return
    fac = _facilities.pop(fac.name, None)
    return fac


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


class ExceptionReporter(IndentedLogWriter):

    def __init__(self, name, env=None, options=None, file=None):
        super().__init__(file=file)
        self.name = name
        self.environment = env
        self.option = IndexedDict(items=options, defaults=_defaultOptions)
        if not file:
            raise ValueError("File not specified")

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
            raise SemtexError(error_text)

    def strict_warning(self, message, loc=None):
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.option.strict or self.option.force_errors:
            raise SemtexError(error_text)
        # warnings.warn("message", SemtexWarning(message))  # UNDONE: says these aren't subclasses of Warning.

    def warning(self, message, loc=None):
        error_text = f'Warning: Invalid Syntax: {message}.'
        self.report(error_text, loc)
        if self.option.force_errors:
            raise SemtexError(error_text)
        # warnings.warn("message", SemtexWarning(message))

    def runtime_error(self, message, loc=None):
        error_text = f'Runtime Error: {message}.'
        self.report(error_text, loc)
        raise SemtexError(error_text)

    def runtime_strict_warning(self, message, loc=None):
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        if self.option.strict or self.option.force_errors:
            raise SemtexError(error_text)
        # warnings.warn("message", SemtexRuntimeWarning(message))

    def runtime_warning(self, message, loc=None):
        error_text = f'Warning: {message}.'
        self.report(error_text, loc)
        if self.option.force_errors:
            raise SemtexError(error_text)
        # warnings.warn("message", SemtexRuntimeWarning(message))

    def report(self, message, loc=None):
        if self.option.stack_trace:
            trace = f'{traceback.print_stack(limit=7)}'
        else:
            trace = ''
        if loc is not None:
            loc.offset -= 1
            carrot = ''
            if self.environment is not None:
                carrot = f'\n\n{self.environment.lines[loc.line]}\n{"^".rjust(loc.offset)}\n' if loc.line < len(self.environment.lines) else ''
            text = f"\n{carrot}\nFOCAL: {message} at position: {loc.line + 1}:{loc.offset}\n\n{trace}"
        else:
            text = f"FOCAL: {message}.\n\n{trace}"
        print(text)


_defaultOptions = {
    'strict': False,
    'force_errors': False,
    'log_file': './semtex.log',
    'stack_trace': False,
}

_facilities = {}
