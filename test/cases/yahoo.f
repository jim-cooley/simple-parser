# trades[> 0] | buys | tail | print

quotes = yahoo( symbols='portfolio.csv', span=-5y )
(open, close, high, low, atr, volume, first, last) = quotes

atr | delay(_, 1d) | atr.plus1 | print

close | sma(_, 10) | close.sma10 | print
close | sma(_, 20) | close.sma20 | print

# close | columns(_, 'AAPL') | delta(_, 1) | signal | print

# print("clipbefore")
# close | delta | signal | clipbefore(_, 1, 0, 1, 0) | print

print("compound")
any:{close > close.sma10, close.sma10 > close.sma20} | signal | clipbefore(_, 1, 0, 1, 0) | signals | print
signals | mul(_, -atr.plus1) | trades | print
trades | cumsum | results | print

# trading results:
results | ret | trading | print

# buy & hold
close | ret | buyhold | print


# num trades:
results > 0 | signal | count(_, axis='c') | x
x[-1] | ntrades | print

# avg per trade:
trading / ntrades | print


# results > 0 | count(_, columns='AAPL') | print
#print("trading")
#trades[trades > 0] | print
#trades > 0 >> buys
#trades < 0 >> sells

#trades[buys] | head | print
#trades[sells] | tail | print

#print("trim")
#close | delta | signal | trim | print



#print('buys =', buys)
#print('sells =', sells)

close | write(_, 'quotes.json', format='json')
