
#
# conversion helpers
#

def c_str2bool(value):
    try:
        i = int(value)
        return bool(i)
    except ValueError as e:
        pass
    try:
        b = bool(value)
        return b
    except ValueError as e:
        pass
    if value.lower() == 'none' or value.lower() == 'empty':
        return False
    return len(value) > 0
