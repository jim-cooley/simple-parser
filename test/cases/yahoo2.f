
read('quotes.csv', format='csv') | close


close | sma(_, 10) | sma10 | print
close | sma(_, 20) | sma20 | print

close | columns(_, 'AAPL') | delta(_, 1) | signal | print

close | delta | signal | print

sma10 > sma20 | signal | x
x > 0 | buys | tail | print
x < 0 | sells | head | print

buys | columns | print
buys | index | transpose | print


buys.head(5)
buys.columns = ['A', 'B', 'C', 'D']
print(buys.columns('A'))

print('buys =', buys)
print('sells =', sells)

print(type(buys))

print(buys.columns)
print(range(0,len(buys.index)))
# buys.columns['E'] = range(0,len(buys.index))  # not mutable
buys['E'] = range(0,len(buys.index))
