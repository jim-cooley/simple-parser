import pandas as pd


def set_print_options():
#   np.set_printoptions(threshold=sys.maxsize)
    return pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 16384,
    )


def print_dataframe(_df, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_df)


def print_series(_s, label=None):
    with set_print_options():
        if label:
            print(label)
        print(_s)