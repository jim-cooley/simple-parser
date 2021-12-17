# wrapper around yahoo quotes
import io
import math
import os
import pandas as pd
import requests as requests

from runtime.conversion import c_unbox
from runtime.factory import to_lit
from runtime.indexdict import IndexedDict
from runtime.scope import Object

from runtime.dataframe import Dataset
from runtime.pandas import print_dataframe
from runtime.runtime import find_file
from runtime.time import Duration, get_t_now

file_suffix = {'1d': 'daily', '1wk': 'weekly'}
config_root = './config/'
data_root = './data/'
report_root = './out/'
data_provider = 'yahoo'

yahoo_base = 'https://query1.finance.yahoo.com/v7/finance/download'
yahoo_5yr = 'range=5y&interval={}&events=history'
yahoo_max = 'range=max&interval={}&events=history'
yahoo_span = 'period1={}&period2={}&interval={}&events=history'

columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

DEFAULT_SPAN_YRS = '5y'
WEEKLY = '1wk'
DAILY = '1d'

_map2freq = {
    DAILY: DAILY,
    'd': DAILY,
    'dy': DAILY,
    'day': DAILY,
    'daily': DAILY,
    WEEKLY: WEEKLY,
    'w': WEEKLY,
    'wk': WEEKLY,
    'week': WEEKLY,
    'weekly': WEEKLY,
}


def init_yahoo(name):
    return {'symbols': None,
            'first': None,
            'last': get_t_now(),
            'span': Duration(DEFAULT_SPAN_YRS),
            'frequency': DAILY,
            'dropna': True,
            'offline': False
            }


def do_yahoo(args):
    """
    fetch yahoo financial stock quotes as a Pandas dataframe.  Parameters passed via 'args'
    :param env:
    :param args:
    :return: Block containing {Open, High, Low, Close, Mean, and Volume}
    """
    symbols = c_unbox(args.symbols)
    if isinstance(symbols, str):
        symbols = read_symbol_list(symbols)
    ds = get_yahoo(symbols=symbols,
                   first=c_unbox(args.first),
                   last=c_unbox(args.last),
                   span=c_unbox(args.span),
                   frequency=_map2freq[args.frequency],
                   dropna=args.dropna,
                   offline=args.offline)

    for key in ds.keys():
        val = ds[key]
        if isinstance(val, pd.DataFrame):
            continue
        elif isinstance(val, dict) or isinstance(val, IndexedDict):
            ds[key] = Dataset(name=key, value=val)
        else:
            ds[key] = to_lit(val=val)
    o = Object()
    o.from_dict(ds)
    return o


def get_yahoo(symbols, first, last, span, frequency, dropna, offline):
    result = dict()
    start = dict()
    end = dict()
    _last = math.floor(last.timestamp())
    _first = math.floor((last + span).timestamp())
    historic = dict({str: pd.DataFrame})
    for sym, row in symbols.iterrows():
        hist = fetch_quotes(sym, _first, _last, frequency, offline)
        if hist is not None and not hist.empty:
            historic[sym] = hist.copy(deep=True)
            start[sym] = hist.index[0]
            end[sym] = hist.index[-1]
    open = zip_historic(historic, 'Open')
    close = zip_historic(historic, 'Adj Close')
    high = zip_historic(historic, 'High')
    low = zip_historic(historic, 'Low')
    atr = zip_historic(historic, 'High', 'Low')
    volume = zip_historic(historic, 'Volume')
    if dropna:
        open.dropna(axis=0, how='any', inplace=True)
        close.dropna(axis=0, how='any', inplace=True)
        high.dropna(axis=0, how='any', inplace=True)
        low.dropna(axis=0, how='any', inplace=True)
        atr.dropna(axis=0, how='any', inplace=True)
        volume.dropna(axis=0, how='any', inplace=True)

    result['open'] = open
    result['close'] = close
    result['high'] = high
    result['low'] = low
    result['atr'] = atr
    result['volume'] = volume
    result['first'] = start  # indicates how much data there is before zip/normalization of the datasets
    result['last'] = end
    if True:
        df = pd.DataFrame([start, end]).transpose()
        df.columns = ['start', 'end']
        print_dataframe(df)
        print(f'\n{len(close.columns)} symbols loaded.\ndates truncated to: {close.index[0]}:{close.index[-1]}\n')
    return result


def fetch_quotes(symbol, start, end, freq, offline=False):
    quotes = pd.DataFrame()
    if offline:
        quotes = read_quotefile(symbol, freq)
    else:
        quotes = _fetch_quotes(symbol, start, end, freq)
    return quotes


def _fetch_quotes(symbol, start, end, interval):
    quotes = None
    quote_url = format_yahoo_url(symbol, start, end, interval)
    headers = {'User-Agent': 'Mozilla/5.0'}  # yahoo is restricting to known user agents as of 06/2021
    with requests.get(quote_url, headers=headers) as response:
        if response.status_code == 200:
            quotes = pd.read_csv(io.StringIO(response.text), index_col='Date')
        else:
            print(f'{quote_url}: response = {response.status_code}\n')
    return quotes


def zip_historic(quotes, column1, column2=None):
    h = pd.DataFrame(columns=['Date'])
    h.set_index('Date', inplace=True)
    keys = sorted(list(quotes.keys())[1:])
    for _s in keys:
        q = pd.DataFrame(quotes[_s])
        if column2 is None:
            q = q.loc[:, [column1]]  # q = q.loc[:, ['Date', column1]]
            q.columns = [_s]  # renames selected column to symbol name
        else:
            qm = pd.DataFrame(q.loc[:, [column1, column2]])
            q = pd.DataFrame(qm.mean(axis=1), columns=[_s])
        h = pd.concat([h, q], axis=1, sort=True)
    return h


def get_quotefilename(basename, folder=None, _suffix=DAILY):
    if _suffix is None:
        return f'{data_root}{basename}.csv' if folder is None else f'{data_root}{folder}/{basename}.csv'
    if _suffix in file_suffix:
        _suffix = file_suffix[_suffix]
        return f'{data_root}{data_provider}/{_suffix}/{basename}_{_suffix}.csv'
    else:
        folder = _suffix if folder is None else folder
        return f'{data_root}{_suffix}/{basename}_{_suffix}.csv'


def read_symbol_list(name):
    symbol_list_filename = find_file(name, extensions=['.csv'])
    symbol_list = create_symbols_table()
    if os.path.isfile(symbol_list_filename) and os.access(symbol_list_filename, os.R_OK):
        ext = get_file_type(symbol_list_filename)
        if ext == '.csv':
            symbol_list = pd.read_csv(symbol_list_filename,
                                      encoding='utf-8',
                                      index_col='symbol',
                                      na_filter=True)
        else:
            group = 'default'
            with open(f'{symbol_list_filename}') as fin:
                for line in fin:
                    _c = line[0]
                    if _c == '#':
                        group = line[1:].strip()
                    elif _c == '(':
                        continue  # like '( line )' is disabled
                    else:
                        fields = line.split('#')
                        if fields:
                            description = ''
                            symbol = fields[0].strip()
                            if len(fields) > 1:
                                description = fields[1].strip()
                            symbol_list = symbol_list.append(
                                {'symbol': symbol, 'group': group, 'description': description}, ignore_index=True)
                symbol_list = symbol_list.set_index('symbol')
    symbol_list = symbol_list.loc[~symbol_list.index.duplicated(keep='first')]
    #   write_symbol_list(name, symbol_list.sort_index())
    return symbol_list


def read_quotefile(symbol, freq):
    quotes = None
    symbol_filename = get_quotefilename(symbol, freq)
    if os.path.isfile(symbol_filename) and os.access(symbol_filename, os.R_OK):
        quotes = pd.read_csv(symbol_filename,
                             encoding='utf-8',
                             index_col='Date',
                             na_filter=True)
    return quotes


def create_symbols_table(symbols=None):
    df = pd.DataFrame(columns=[
        'symbol', 'group', 'description'
    ])
    if symbols:
        df.append(symbols)
    return df


def get_file_type(file_path):
    fn_ext = os.path.splitext(file_path)
    return fn_ext[1].lower() if fn_ext[1] else '.txt'


def get_config_filename(file_path, suffix=None, ext='.txt'):
    file_path = file_path.lower()
    fn = os.path.split(file_path)
    path = fn[0] if fn[0] else config_root
    fn_ext = os.path.splitext(file_path)
    file_name = fn_ext[0]
    ext = fn_ext[1] if fn_ext[1] else ext
    return f'{path}{file_name}{suffix}{ext}' if suffix else f'{path}{file_name}{ext}'


def format_yahoo_url(symbol, start, end, interval):
    return f'{yahoo_base}/{symbol}?{yahoo_span.format(start, end, interval)}'


def format_yahoo_5yr_url(symbol, interval):
    return f'{yahoo_base}/{symbol}?{yahoo_5yr.format(interval)}'


def format_yahoo_max_url(symbol, interval):
    return f'{yahoo_base}/{symbol}?{yahoo_max.format(interval)}'
