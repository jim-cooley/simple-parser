# parsing and semantic analysis exception handling and helper functions
import traceback
from copy import deepcopy

from runtime.indexdict import IndexedDict
from runtime.logwriter import IndentedLogWriter


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


def getLogFacility(name, options=None, lines=None, file=None):
    if name not in _facilities:
        f = ExceptionReporter(name, lines=lines, options=options, file=file)
        _facilities[name] = f
    return _facilities[name]


def removeLogFacility(fac):
    if fac.name not in _facilities:
        return
    fac = _facilities.pop(fac.name, None)
    return fac


def setLogConfiguration(name, options, lines=None):
    f = getLogFacility(name, options, lines)
    f.set_options(options)
    f.lines = lines


def runtime_error(message, loc=None):
    f = getLogFacility('focal')
    f.runtime_error(message, loc)


# strict warning becomes error if option.strict is true (variable used before being declared)
def runtime_strict_warning(message, loc=None):
    f = getLogFacility('focal')
    f.runtime_strict_warning(message, loc)


def runtime_warning(message, loc=None):
    f = getLogFacility('focal')
    f.runtime_warning(message, loc)


class ExceptionReporter(IndentedLogWriter):

    def __init__(self, name, lines=None, options=None, file=None):
        super().__init__(file=file)
        self.name = name
        self.lines = lines
        self.option = IndexedDict(items=options, defaults=_defaultOptions)
        if not file:
            raise ValueError("File not specified")

    def set_lines(self, lines):
        """sets the source lines used for reporting errors & warnings"""
        self.lines = deepcopy(lines)

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
            if self.lines is not None:
                carrot = f'\n\n{self.lines[loc.line]}\n{"^".rjust(loc.offset)}\n' if loc.line < len(self.lines) else ''
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
