# mimic a set of trading rules
# reserved words: 'position', 'trades', 'portfolio'
#
trades1_tests = [
    "def atr = (high + low) / 2; median = (close + open) /2",
    "def trade_size = postition * 10%",
    "any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy",
    "close <| sma(10) | signal >> delay(1d) | atr => sell",
    "buy: position += trade_size",
    "trades",   # display trades table
    "trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price')",
]
