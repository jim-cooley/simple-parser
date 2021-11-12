from datetime import datetime
from environment.literals import Time
from environment.exceptions import getLogFacility
from environment.scope import IntrinsicFunction


# -----------------------------------
# Intrinsic Functions
# -----------------------------------
# format is: do_ is called by Invoke and handles any parameter validation / massaging.
#            init_ is called by keword_init to load the function descriptors and default parameters
#            get_ is used by internal functions to retrieve the results of the intrinsic without the parameter
#                 manipulation and will be called with native types as input.  Internal types are returned by convention

# Now, Today
# -----------------------------------

def do_now(env=None):
    return get_now()


def get_now():
    return Time(datetime.now())


# Print
# -----------------------------------
def init_print(name):
    return IntrinsicFunction(name=name,
                             defaults={
                                 'message': '',
                                 'format': None,
                             })


def do_print(env, args):
    form = args.format
    logger = getLogFacility('semtex')
    if form is not None:
        _t_print(logger, form.format(args.message))
    else:
        _t_print(logger, args.message)
    return args.message


def _t_print(logger, message, end='\n'):
    if logger is None:
        logger = getLogFacility('semtex')
    logger.write(f'{message}', end=end)
    logger.flush()
