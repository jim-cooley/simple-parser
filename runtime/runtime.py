import os

# -------------------------------------------------
# Routines environment amongst the Intrinsic Functions
# -------------------------------------------------
from runtime.options import getOptions

_BASE_SEARCH_PATH = [
    ".",
    "./etc",
    "./etc/config",
    "./test",
    "./test/cases",
    "./scripts",
    "./etc/scripts",
]
_DEFAULT_EXTENSIONS = [
    ".f",
    ".p",
    ".t",
    ".csv",
]


def find_file(name, search_paths=None, extensions=None):
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


def load_file(fname, search_paths=None):
    fname = find_file(fname, search_paths=search_paths)
    name = os.path.splitext(os.path.basename(fname))[0]
    ext = os.path.splitext(fname)[1]
    idx = 0
    with open(fname, 'r') as file:
        text = file.read()
    return text
