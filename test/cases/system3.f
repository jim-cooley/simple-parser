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

    print("max draw down (per share, $)")
    results | min | print

    print("num trades")
    results > 0 | signal | count(_, axis='c') | x
    x[-1] >> ntrades | transpose | print

    print("avg per trade")
    returns / ntrades | transpose | print

    print("rating")
    rules[-1] | transpose | rename(_, 0, 'rating') | replace({true: 'buy', false:'sell'}) | print

    print("trade sheet")
    signals[-1] | transpose | print

    signals[-1] | transpose | rename(_, 0, 'signal') | y
    print("sells:")
    select(y, "signal < 0") | print

    print("buys:")
    select(y, "signal > 0") | print

    return returns
}

rules = any:{
    close > close.sma10,
    close > close.sma20,
}

print("close_sma10_cross")
df["close_sma10_cross"] = analyze(rules=close_sma10_cross)

print("close_sma20_cross")
#df["close_sma20_cross"] = analyze(rules=close_sma20_cross)

print("close_sma_10_20_cross")
#df["close_sma_10_20_cross"] = analyze(rules=close_sma_10_20_cross)

print("test rules:")
#df["rules"] = analyze(rules=rules)

print("comparison %")
print(df)





