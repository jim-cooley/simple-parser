# Data Types
> <h2>*what's the difference between set, tuple, and block?*</h2>

type | description
--- | ---
`block` | Contains statements and expressions, with k:v pairs defining symbols w/in scope
`dataset` / `dataframe` | Pandas DataFrame.  </br>NOTE: will likely be merged into `set` 
`list` | Sequenctial, ordered, iterable, heterogeneous, allows duplicates, nestable
`tuple` | Sequenctial, ordered, iterable, heterogeneous, allows duplicates, nestable </br>Can be used to assign to multiple variables.  parameter list
`set` | Contains statements, and expressions, with k-v pairs (but could be anonymous?) </br>Unordered, heterogeneous, no duplicates (coalesced), nestable

## parsing

parser expression | code | alternate
--- | --- | ---
`tuple = '(' + item + [',' + item]* + ')'` | tuple() | ()
`list = '[' + item + [',' + item]* + ']'` | list() | []
`set = '{' + item + [',' + item]* + ']'` | set()
`dictionary = '{' + key:value + [',' + key:value]* + '}'` | dict() | {}

## other datatypes

type | description | notes
--- | --- | ---
`int` | `int64` | do we support uint64?
`category` | `Enum` | categorical value
`duration` | `timedelta64` |
`enumeration` | `IntEnum` | categorical values with numeric equivalents
`float` | `float64` |
`object` | `object` | unknown, late-bound access
`str` | `str` |
`time` | `datetime` |

&nbsp;

> NOTE: we need to support category types as well as other integer, float, date, time precisions for Pandas & NumPy

