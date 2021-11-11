from datetime import datetime
from literals import Time


# -----------------------------------
# Intrinsic Functions
# -----------------------------------
# format is: do_ is called by Invoke and handles any parameter validation / massaging.
#            init_ is called by keword_init to load the function descriptors and default parameters
#            get_ is used by internal functions to retrieve the results of the intrinsic without the parameter
#                 manipulation and will be called with native types as input.  Internal types are returned by convention

def do_now():
    return get_now()


def get_now():
    return Time(datetime.now())

