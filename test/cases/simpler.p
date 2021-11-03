rules0a := {
    buy:: any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal | delay(1d) | atr,
    sell:: close <| sma(10) | signal | delay(1d) | atr
}
rules0 := {
    close >| sma(10) | signal | delay(1d) | atr | buy,
    close <| sma(10) | signal | delay(1d) | atr | sell
}
rules1 => {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr -> sell
}
rules2 := {
    buy: any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr,
    sell: close <| sma(10) | signal >> delay(1d) | atr
}
rules3 := {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr -> sell
}
rules4 = {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr -> sell
}
def rules5 = {
    any:{ close >| sma(10), close >| sma(20) }:(threshold=0.01) | signal >> delay(1d) | atr => buy,
    close <| sma(10) | signal >> delay(1d) | atr -> sell
}
