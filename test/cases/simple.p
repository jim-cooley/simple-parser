# sample rules file for pyser / qtradr

def atr = (high + low) / 2
def median_price = (open + close) / 2
def trade_size = position * 10%

rules = {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr => sell
}
buy:: position += trade_size
sell:: position -= trade_size

# %%report: trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price')

