# Boolean Operations

## Truthiness (boolean conversion):
Type | Value(s) | T / F
--- | --- | ---
datetime | |
duration | dur(0) | false
| | _nonzero_ | true
float | 0.0 | false
| | _nonzero_ | true
int | 0 | false
| | _nonzero_ | true
none | _none_ | false
set | {} | false
str | `'nil'`, `'none'`, `'empty'`, `'false'`, `'False'`, `'0'`, `len(str) = 0` | false
| | _otherwise_ | true


## Unary Operations

### _not_ 

Type | Value(s) | Result
--- | --- | ---
bool | false | true
| | true | false
datetime | |
datetime | dur(0) | true
| | _otherwise_ | false
float | 0.0 | true
| | _otherwise_ | false
int | 0 | true
| | _otherwise_ | false
str | `'nil'`, `'none'`, `'empty'`, `'false'`, `'False'`, `'0'`, `len(str) = 0` | true
| | _otherwise_ | false

_In all cases, the result type is boolean_

## Binary Order Comparisons

