# Language Examples

## sample rules file for qtradr system
The following is an illustration of using Focal to implement a trading system backtest

```
periods = {
    'train': (today-2y)..today
}

var sma_periods1 = [3,5,10..20,28]
var sma_periods2 = [5,10,12,20,30,60,90]

(open, high, low, close, adj_close) = yahoo( file='spq500.csv', periods['train5'] )
atr = (high + low) / 2
median_price = (open + close) / 2
price10a := _.delay(1d)[10:00]

report := { trades(buy, sell) | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') }

rules := {
    baseline = {
        any:{ close |> sma(10), close |> sma(20), sma(10) |> sma(20) }:(threshold=0.01) | signal(close) >> delay(1d) -> buy(atr),
        close <| sma(10) | signal(close) >> delay(1d) -> sell
    },
    scenario1 = {
        { close |> sma(r2) } | delay(1d) | signal(atr)  -> buy,
        close <| sma(r1) | delay(1d) | signal(atr) -> sell
    },
    scenario2 = {
        { close |> sma(r1) }:(threshold=0.01) | delay(1d) | signal -> buy,
        close <| sma(r1) | delay(1d) | signal -> sell
    },
    scenario3 = {
        { sma(r1) |> sma(r2) } | delay(1d) | signal -> buy,
        close <| sma(r1) | delay(1d) | signal -> sell
    },
    {
        { close |> sma(r1) } | delay(1d) | signal -> buy,
        close <| sma(r2) | delay(1d) | signal -> sell
    }
}

backtest( rules:{r1=sma_periods1, r2=sma_periods2}, period=period['train'])
rules => report | print
```

## discussion
Now, lets walk through what is happening in this example:

### Step 1
```
periods = {
    'train': (today-2y)..today  # also range(-2y) would work
}
```
This sets up a _Dictionary_ with a named range representing the duration of the last 2yrs, with a comment as to an alternate syntax for this.

### Step 2
```
var sma_periods1 = [3,5,10..20,28]
var sma_periods2 = [5,10,12,20,30,60,90]
```
This establishes two lists of values to be used for the backtest later on.  The keyword `var` indicates that these variables will may take on any value in the set, this is akin to defining them as a range() with explicit values.  Here, the intrinsic `range` is implied later on when they are used.

### Step 3
```
(open, high, low, close, adj_close) = yahoo( file='spq500.csv', periods['train5' )
```
Here, we download historic stock data for the period of the simulation using the `yahoo` intrinsic function.  The output from yahoo finance(tm) includes the colums `open`, `high`, `low`, `close`, `adj_close`; these are assigned to the separate data series: `open`, `high`, `low`, `close`, `adj_close`

#### Step 4
```
atr = (high + low) / 2
median_price = (open + close) / 2
```
Two new data series are produced via derivation from the historic data.  This is `atr` or Average Trading Range, and `median` to denote Median Daily Price.

#### Step 5
```
price10a := _.delay(1d)[10:00]
```
This defines an inline transform that will enable subscripting on an existing datastream, for example: `price.price10a` would be equivalent to `price.delay(1d)[10:00]`.  This is also equivalent to `price | delay(1d) | select(time=10:00)`

#### Step 6
```
report := { trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price') }
```
This sets up an inline function to use when reporting.  When `report` is invoked, it will transform into `trades | select('symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price')`

#### Step 7
```
rules := {
```

This defines a _Block_ containing what will be the 'rules' used in the backtest.  In this case 'rules' are just named expressions that will be evaluated later.  Lets explain these one at a time.

#### Step 8
```
baseline = {
    any:{ close |> sma(10), close |> sma(20), sma(10) |> sma(20) }:(threshold=0.01) | signal(close) >> delay(1d) -> buy(atr),
    close <| sma(10) | signal >> delay(1d) -> sell(atr)
},
```
This etablishes a named set of expressions called `baseline`.  In the backtest later on, it will be the set of values that we compare others to, but the name `backtest` serves no special purpose other than to denote this for ourselves.

#### Step 9
```
any:{ close |> sma(10), close |> sma(20), sma(10) |> sma(20) }:(threshold=0.01) | signal(close) | delay(1d) -> buy(atr),
```
This is a parameterized set with a set operator `all:` applied.  It indicates that _all_ of the mebers of the set must be true to indicate success.  The execution of this will evaluate the subexpressions `close |> sma(10)` which is true where the close series values rise above the series `sma(10)`.  `sma` is an intrinsic which evaluates to the _Simple Moving Average_ of the data series.  When that is not specified (as in: `close.sma(10)`), then focal takes that to be applied to the argument of the lefthand side.  Equivalent to `close |>= sma(10)` if there was such an operator.  The `:(threshold=0.01)` is known as a `set parameter`, or a `parameterization expression`.  This sets up the key:value pair of `threshold=0.01` to be available by the items in the inner block.  Essentially _injecting_ a parameter into the block.  In this case, that is used by the `|>` and `<|` operators to indicate at what precision the crossing detection is made.
&nbsp;
The above expression evaluates to a new series with True appearing where the expression evaluates to True, and False otherwise.  This new series is transformed by the `signal` intrinsic function which translates this into a new series with the values from the `close` series replacing True and `0` replacing False.
&nbsp;
This series is delayed by 1d and then used to raise a `buy` signal using the _Average Trading Range_ series.  In this example, `buy` is an intrinsic, but this could be any function.  The _raise_ operator `->` invokes the function on the righthand side for each value of the lefthand side that evaluates to True (nonzero)
&nbsp;
This example is a little contrived to show the expressive nature of Flow equations but could be simplified to</br>
` | delay(1d) -> buy(atr)` or `| signal(close) | delay(1d) -> buy`


