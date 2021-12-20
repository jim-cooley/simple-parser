from datetime import datetime

import pandas as pd
from runtime.dataframe import Dataset
from runtime.indexdict import IndexedDict
from runtime.pandas import print_dataframe
from runtime.exceptions import getLogFacility


_default_options = {
    'width': 16484,
    'full': True,
    'max_rows': 20,
    'max_columns': 20,
}


# Print
# -----------------------------------
def init_print(name):
    return {'message': ''}


def do_print(args=None):
    logger = getLogFacility('focal')
    line = []
    options = _default_options
    if hasattr(args, 'options'):
        options.update(_parse_print_options(args.options))
    options = IndexedDict(options)
    args.remove('options')
    for i in range(0, len(args)):
        o = args[i]
        line.append(_print_item(o, options))
    text = ' '.join(line)
    _t_print(logger, text)
    return text


def _print_item(o, options):
    line = []
    if isinstance(o, list):
        for i in o:
            line.append(_print_item(i, options))
        if len(line) > 20:
            text = '\n'.join(line)
        else:
            text = ', '.join(line)
        return f'[{text}]'
    elif isinstance(o, str):
        line.append(o.replace("\\n", "\n"))
    elif isinstance(o, Dataset) or isinstance(o, pd.DataFrame):
        print_dataframe(o, options=options)
    elif isinstance(o, datetime):
        line.append(datetime.isoformat(o))
    else:
        if hasattr(o, 'print'):
            o.print()
        else:
            if hasattr(o, 'format'):
                text = o.format()
            else:
                text = f'{o}'
            line.append(text)
    text = ' '.join(line)
    return text


def _parse_print_options(optstr):
    po = optstr.split(',')
    options = {}
    for k in po:
        kv = k.split('=')
        if len(kv) == 1:
            options[kv[0]] = True
        else:
            options[kv[0]] = kv[1]
    return options


def _t_print(logger, message, end='\n'):
    if logger is None:
        logger = getLogFacility('focal')
    logger.write(f'{message}', end=end)
    logger.flush()
