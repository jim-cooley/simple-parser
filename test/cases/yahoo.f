
quotes = yahoo( symbols='portfolio.csv', span=-5y )
close = quotes.close

close | sma(_, 10) | sma10 | print
close | sma(_, 20) | sma20 | print

close | columns(_, 'AAPL') | delta(_, 1) | signal | print

close | delta | signal | print

sma10 > sma20 | signal | x
x > 0 | buys | tail | print
x < 0 | sells | head | print


print('buys =', buys)
print('sells =', sells)

print(close[-1])
print(close[:-1])
print(close[3:])
print(close[1:10])
print(close[::2])
print(close[:10:2])
print(close[1:10:2])


close | write(_, 'quotes.json', format='json')
