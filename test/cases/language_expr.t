close.sma(13) | signal(price, how='>')
any:{ close >| sma(10), close <| sma(20) }:(threshold=0.01) | signal >> avg | delay(1d) | buy
atr = (high - low) / 2; med = (close - open) /2
any:{ close >| sma(10), close <| sma(20) }:(threshold=0.01) | signal >> atr | delay(1d) => buy
any:{ cross(close, sma(20), delay=1, threshold=0.01) } | buy
pcross(close, sma(13)) | smacd(close, 20, 50) | smacd.close(20,50) | close.smacd(20,50)
(close.sma(20) and close.sma(50)) | diff | sign | signal(how='cross')
{close.sma(20) and close.sma(50)} | diff | sign | signal(how='cross')
open.delay(1d) | buy
start: open.delay(1d) | buy
close >| sma(10) and close <| sma(20)
close >| sma(10) and close <| sma(20) | signal
close >| sma(10) and close <| sma(20) | signal >> open.delay(1d)
close >| sma(10) and close <| sma(20) | signal >> open.delay(1d) | buy
start: open.delay(1d) | buy; end: open | sell
close >| sma(20) | signal | open.delay(1d) | buy; close <| sma(10) | signal | open.delay(1d) | sell
