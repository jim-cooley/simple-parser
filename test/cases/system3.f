periods = {
    train: [(today-2y),today]
    index = ['start', 'end']
    columns = ['train']
}
sma_period = [3,5,10..20,28]
print(sma_period)
print(periods)


read('quotes.csv', format='csv') | close

# productions: new datasets
report(trades) := { trades | columns(_, 'symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') | print }

