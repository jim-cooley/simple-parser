# sample rules file for pyser / qtradr
%%backtest [period='train5', rules=rules]

atr := (high + low) / 2
median_price := (open + close) / 2
trade_size := position * 10%

def buy = { position += trade_size }
def sell = { position -= trade_size }

rules => {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr -> sell
}

report := { trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') }

%%report {report}

