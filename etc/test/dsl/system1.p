# sample rules file for pyser / qtradr

%%yahoo (file='spq500.csv', 2y)
%%backtest (rules, period='train')
%%report { report >> rules }

#
periods = {
    'train': today-2y..today
}
sma_period = [3,5,10..20,28]

# productions: new datasets
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
        { close >| sma(20) } | signal >> atr.delay(1d) => buy,
        close <| sma(10) | signal >> atr.delay(1d) => sell
    },
    scenario2 = {
        { close >| sma(10) }:(threshold=0.01) | signal >> atr.delay(1d) => buy,
        close <| sma(10) | signal >> atr.delay(1d) => sell
    },
    scenario3 = {
        { sma(10) >| sma(20) } | signal >> atr.delay(1d) => buy,
        close <| sma(10) | signal >> atr.delay(1d) => sell
    },
    {
        { close >| sma(sma_period) } | signal >> atr.delay(1d) => buy,
        close <| sma(sma_period) | signal >> atr.delay(1d) => sell
    }
}
