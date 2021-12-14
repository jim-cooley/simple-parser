# sample rules file for pyser / qtradr
#
periods = {
    train: (today-2y)..today
}
sma_period = [3,5,10..20,28]

read('quotes.csv', format='csv') | close


# productions: new datasets
report := { trades | columns('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') | print }


rules: {
    baseline = {
        buy: any:{ close >| sma(10), close >| sma(20), sma(10) >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr,
        sell: close <| sma(10) | signal >> delay(1d) | atr
    },
    scenario = {
        buy: { close >| sma(sma_period) } | signal >> atr.delay(1d),
        sell: close <| sma(sma_period) | signal >> atr.delay(1d)
    }
}
