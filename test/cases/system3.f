quotes = yahoo( symbols='portfolio.csv', span=-5y )
(open, close, high, low, atr, volume, first, last) = quotes

atr.plus1 = delay(atr, 1d)
close.sma10 = sma(close, 10)
close.sma20 = sma(close, 20)
buyhold = ret(close)

close_sma10_cross = close > close.sma10
close_sma20_cross = close > close.sma20
close_sma_10_20_cross = close.sma10 > close.sma20

df = dataframe
df["buyhold"] = buyhold

analyze(rules) := {
    rules | signal | clipbefore(_, 1, 0, 1, 0) >> signals

    print("signals")
    signals | mul(_, -atr.plus1) >> trades | print

    print("cummulative returns")
    trades | cumsum >> results | print

    print("trading results")
    results | ret >> trading | print

    print("num trades")
    results > 0 | signal | count(_, axis='c') | x
    x[-1] >> ntrades | print

    print("avg per trade")
    trading / ntrades | print

    return trading
}

rules = any:{
    close > close.sma10,
    close > close.sma20,
    close.sma10 > close.sma20
}

print(analyze(rules=close_sma10_cross))

print("close_sma10_cross")
df["close_sma10_cross"] = analyze(rules=close_sma10_cross)

print("close_sma20_cross")
df["close_sma20_cross"] = analyze(rules=close_sma20_cross)

print("close_sma_10_20_cross")
df["close_sma_10_20_cross"] = analyze(rules=close_sma_10_20_cross)

print("test rules:")
df["rules"] = analyze(rules)

print("comparison")
print(df)





