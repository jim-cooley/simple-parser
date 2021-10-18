shell_tests = [
    "%%backtest",
    "%%load_quotes(file='./etc/spq500.csv'); backtest(period='train5'); report('trades', 'stops')",
]