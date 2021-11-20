from datetime import datetime

from runtime.dataframe import Dataset
from runtime.literals import Time


# -----------------------------------
# Intrinsic Functions
# -----------------------------------
# format is: do_ is called by Invoke and handles any parameter validation / massaging.
#            init_ is called by keword_init to load the function descriptors and default parameters
#            get_ is used by internal functions to retrieve the results of the intrinsic without the parameter
#                 manipulation and will be called with native types as input.  Internal types are returned by convention

# Now, Today
# -----------------------------------
from runtime.series import Series


def do_now(env=None):
    return get_t_now()


def get_t_now():
    return Time(datetime.now())


def get_dt_now():
    return datetime.now()


def create_dataset(env=None, args=None):
    d = Dataset()
    return d


def create_series(env=None, args=None):
    r = Series()
    return r
