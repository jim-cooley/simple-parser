sma(10)
fn_with_parameters(1,2,3,4)
close.delay(1d)
close.delay[+1d]
close[+1d]
close.weekly.sma(20)
close[weekly].sma(20)
close{weekly}.sma(20)
f(a = 5)
x(a = 5, b='a')
#:(a = 5)   - now syntax error
#:(a = 5, b='a')  - now syntax error
(a = 5)
(a = 5, b='a')
#:(a = 5) - now syntax error
#:(a = 5, b='a') - now syntax error
f(a = 5,)
x(a = 5, b='a',)
(a = 5,)
a:(a = 5)
{a}:(a = 5)
a:{a,b,c}:(a = 5)
{a,b,c}:{a = 5}
{a,b,c}:(a = 5)
