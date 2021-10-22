# sample rules file for pyser / qtradr

periods = {
    'train': today-2y..today
}
sma_periods1 = [3,5,10..20,28]
sma_periods2 = [5,10,12,20,30,60,90]

var r = range(sma_periods1)
var r2 = range(in sma_periods2)

(open, high, low, close, adj_close) = yahoo( file='spq500.csv', 2y )
atr = (high + low) / 2
median_price = (open + close) / 2
price10a = price.delay(1d)[10:00]

report := { trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') }

rules: {
    baseline = {
        any:{ close >| sma(10), close >| sma(20), sma(10) >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
        close <| sma(10) | signal >> delay(1d) | atr -> sell
    },
    scenario1 = {
        { close >| sma(r2) } | signal >> atr.delay(1d) => buy,
        close <| sma(r1) | signal >> atr.delay(1d) => sell
    },
    scenario2 = {
        { close >| sma(r1) }:(threshold=0.01) | signal >> atr.delay(1d) => buy,
        close <| sma(r1) | signal >> atr.delay(1d) => sell
    },
    scenario3 = {
        { sma(r1) >| sma(r2) } | signal >> atr.delay(1d) => buy,
        close <| sma(r1) | signal >> atr.delay(1d) => sell
    },
    {
        { close >| sma(r1) } | signal >> atr.delay(1d) => buy,
        close <| sma(r2) | signal >> atr.delay(1d) => sell
    }
}

backtest( rules, period=period['train'])
report >> rules | print
