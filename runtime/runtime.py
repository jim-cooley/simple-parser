import os

# -------------------------------------------------
# Routines environment amongst the Intrinsic Functions
# -------------------------------------------------

_BASE_SEARCH_PATH = [
    ".",
    "./etc",
    "./etc/config",
]
_DEFAULT_EXTENSIONS = [
    ".f",
    ".csv",
]


def _find_file(name, search_paths=None, extensions=None):
    extensions = extensions or _DEFAULT_EXTENSIONS
    search_paths = search_paths or _BASE_SEARCH_PATH
    for path in search_paths:
        fname = f'{path}/{name}'
        if os.path.isfile(fname):
            return fname
        for x in extensions:
            if os.path.isfile(f'{fname}{x}'):
                return f'{fname}{x}'
    raise IOError(f'invalid filename: {name}, cannot be found or is not a file')