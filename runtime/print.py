from runtime.dataframe import Dataset, print_dataframe
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
    logger = getLogFacility('focal')
    line = []
    for i in range(0, len(vargs)):
        o = vargs[i]
        if isinstance(o, Dataset):
            print_dataframe(o)
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
    _t_print(logger, text)
    return vargs.message


def _t_print(logger, message, end='\n'):
    if logger is None:
        logger = getLogFacility('focal')
    logger.write(f'{message}', end=end)
    logger.flush()
