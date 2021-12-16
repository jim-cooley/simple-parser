# trades[trades > 0] | buys | tail | print

quotes = yahoo( symbols='portfolio.csv', span=-5y )
(open, close, high, low, atr, volume, first, last) = quotes

atr | delay(_, 1d) | atr.plus1 | print


close | sma(_, 10) | close.sma10 | print
close | sma(_, 20) | close.sma20 | print

close | columns(_, 'AAPL') | delta(_, 1) | signal | print

close | delta | signal | print

close.sma10 > close.sma20 | signal | mul(_, -atr.plus1) | trades | print

print("trading")
trades > 0 | buys | tail | print
trades < 0 | sells | head | print


trades | cumsum | results | print

results | tail(_, 20) | print


print('buys =', buys)
print('sells =', sells)

close | write(_, 'quotes.json', format='json')
