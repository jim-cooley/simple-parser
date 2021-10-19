trades2_tests = [
    "atr = (high + low) / 2; median = (close + open) /2",
#    "range:(3, 5, 10..20, 50, 90)", # ranges need modifications to Float scanning
    "any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy",
    "close <| sma(10) | signal >> delay(1d) | atr => sell",
]
