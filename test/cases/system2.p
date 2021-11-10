periods = {
    'train': (today-2y)..today
}

var sma_periods1 = [3,5,10..20,28]
var sma_periods2 = [5,10,12,20,30,60,90]

(open, high, low, close, adj_close) = yahoo( file='spq500.csv', periods['train5'] )
atr = (high + low) / 2
median_price = (open + close) / 2
price10a := _.delay(1d)[10:00]

report := { trades(buy, sell) | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') }

rules := {
    baseline = {
        any:{ close |> sma(10), close |> sma(20), sma(10) |> sma(20) }:(threshold=0.01) | signal(close) >> delay(1d) -> buy(atr),
        close <| sma(10) | signal(close) >> delay(1d) -> sell
    },
    scenario1 = {
        { close |> sma(r2) } | delay(1d) | signal(atr)  -> buy,
        close <| sma(r1) | delay(1d) | signal(atr) -> sell
    },
    scenario2 = {
        { close |> sma(r1) }:(threshold=0.01) | delay(1d) | signal -> buy,
        close <| sma(r1) | delay(1d) | signal -> sell
    },
    scenario3 = {
        { sma(r1) |> sma(r2) } | delay(1d) | signal -> buy,
        close <| sma(r1) | delay(1d) | signal -> sell
    },
    {
        { close |> sma(r1) } | delay(1d) | signal -> buy,
        close <| sma(r2) | delay(1d) | signal -> sell
    }
}

backtest( rules:{r1=sma_periods1, r2=sma_periods2}, period=period['train'])
rules => report | print
