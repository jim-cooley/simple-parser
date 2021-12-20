quotes = yahoo( symbols='portfolio.csv', span=-2y )
(open, close, high, low, atr, volume, first, last) = quotes

atr.plus1 = delay(atr, 1d)
close.sma10 = sma(close, 10)
close.sma20 = sma(close, 20)
buyhold = ret(close)
close.min = close | min

close_sma10_cross = close > close.sma10
close_sma20_cross = close > close.sma20
close_sma_10_20_cross = close.sma10 > close.sma20

df = dataframe
df["buyhold"] = buyhold

analyze(rules) := {
    rules | signal | clipbefore(_, 1, 0, 1, 0) >> signals
    signals | mul(_, -atr.plus1) >> trades
    trades | cumsum >> results
    results | ret >> returns

    print("\nmax draw down (per share, $)")
    results | min | print

    print("\nnum trades")
    results > 0 | signal | count(_, axis='c') | x
    x[-1] >> ntrades | transpose | print

    print("\navg % return per trade")
    returns / ntrades | transpose | print

    print("\ncurrent rating")
    rules[-1] | transpose | rename(_, 0, 'rating') | replace(_, {true: 'buy', false:'sell'}) | print
    signals[-1] | transpose | rename(_, 0, 'signal') | y
    # y | replace(_, {-1:'sell', 1:'buy'}) | print

    print("\nsells:")
    select(y, "signal < 0") | replace(_, {-1: 'sell',}) | print

    print("\nbuys:")
    select(y, "signal > 0") | replace(_, {1: 'buy',}) | print

    return returns
}

rules = any:{
    close > close.sma10,
    close > close.sma20,
}

print("\n\nclose_sma10_cross")
df["close_sma10_cross"] = analyze(rules=close_sma10_cross)

print("\n\nclose_sma20_cross")
#df["close_sma20_cross"] = analyze(rules=close_sma20_cross)

print("\n\nclose_sma_10_20_cross")
#df["close_sma_10_20_cross"] = analyze(rules=close_sma_10_20_cross)

print("\n\ntarget rules:")
#df["rules"] = analyze(rules=rules)

print("\n\ncomparison %")
print(df)





