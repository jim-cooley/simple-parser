import pandas as pd

from runtime.dataframe import Dataset
from runtime.exceptions import getLogFacility
from runtime.scope import IntrinsicFunction


# Print
# -----------------------------------
def init_print(name):
    return IntrinsicFunction(name=name,
                             defaults={
                                 'message': '',
                             })


def do_print(env, vargs):
    logger = getLogFacility('semtex')
    line = []
    for i in range(0, len(vargs)):
        o = vargs[i]
        if isinstance(o, Dataset):
            print_dataframe(o)
        else:
            if hasattr(o, 'format'):
                text = o.format()
            else:
                text = f'{o}'
            line.append(text)
    text = ' '.join(line)
    _t_print(logger, text)
    return vargs.message


def _t_print(logger, message, end='\n'):
    if logger is None:
        logger = getLogFacility('semtex')
    logger.write(f'{message}', end=end)
    logger.flush()


def print_dataframe(_df, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_df)


def set_print_options():
#   np.set_printoptions(threshold=sys.maxsize)
    return pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 16384,
    )