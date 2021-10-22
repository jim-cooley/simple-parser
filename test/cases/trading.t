def atr = (high + low) / 2; median = (close + open) /2
def trade_size = postition * 10%
any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy
close <| sma(10) | signal >> delay(1d) | atr => sell
buy: position += trade_size
trades
trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price')
atr = (high + low) / 2; median = (close + open) /2
any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy
close <| sma(10) | signal >> delay(1d) | atr => sell
#    "range:(3, 5, 10..20, 50, 90)", # ranges need modifications to Float scanning
