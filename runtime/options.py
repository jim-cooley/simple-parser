from runtime.indexdict import IndexedDict
"""
Options - This provides a global option facility based on IndexedDict()
"""
_optionFacilities = {}


def getOptions(name, options=None, defaults=None):
    if name not in _optionFacilities:
        o = IndexedDict(items=options, defaults=defaults)
        _optionFacilities[name] = o
    return _optionFacilities[name]


def getOption(name, option, default):
    if name in _optionFacilities:
        options = _optionFacilities[name]
        if option in options:
            return options[option]
    return default


