
x => x:x + 1

sugar(x) => { x + 1 }

sugar(x) := { x + 1 }

sugar(x) = { x + 1 }

def simple(x) := {
    x + 1
}

def factorial(x) := {
    if x == 1 then
        return 1
    else
        x * factorial(x - 1)
}

# simple inline functions
a := 3
a := a + 1
a => a + 1

# inline functions:
def atr = (high + low) / 2
def avg_daily_price = (open + close) / 2
def trade_size = position * 10%
atr := (high + low) / 2
avg_daily_price := (open + close) / 2
trade_size := position * 10%

# from tuples:
(a, b, c,)                   # tuple
(a, b, c) = (4, 5, 6)        # tuple assignment
(a, b, c) := (4, 5, 6)       # tuple assignment (var)
(a, b, c) = (a:5, b:3, c:4)  # tuple assignment k:v
{a, b, c}:(4, 5, 6)          # set parameterization
{a, b, c}:(a:5, b:3, c:4)    # set parameterization k:v
{a, b, c}:(a=5, b=3, c=4)    # set parameterization k=v (error?)
{a, b, c}:{a=5, b=3, c=4}    # set parameterization k=v (block)
{a, b, c}:{a:5, b:3, c:4}    # set parameterization k=v (block)


