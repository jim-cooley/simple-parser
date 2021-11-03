# Data Types
> <h2>*what's the difference between set, tuple, and block?*</h2>
#
type | description
--- | ---
block | contains statements and expressions
set | contains statements, and expressions, with k-v pairs (but could be anonymous?)
list, tuple | sequenctial, ordered, iterable, heterogeneous, allows duplicates, nestable
set | unordered, heterogeneous, no duplicates (coalesced), nestable
dictionary | k,v pairs

## parsing

parser expression | code | alternate
--- | --- | ---
`tuple = '(' + item + [',' + item]* + ')'` | tuple() | ()
`list = '[' + item + [',' + item]* + ']'` | list() | []
`set = '{' + item + [',' + item]* + ']'` | set()
`dictionary = '{' + key:value + [',' + key:value]* + '}'` | dict() | {}
