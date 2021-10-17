trades2_tests = [
    "atr = (high + low) / 2; median = (close + open) /2",
    "any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy",
    "close <| sma(10) | signal >> delay(1d) | atr => sell"
]