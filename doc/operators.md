# Operator Precedence

Precedence | Operator | Description | Associativity
:---: | :---: | --- | :---: |
0 | `(`..`)` | grouping |
1 | `.` | qualification |
| | `[`..`]` | index expression |
2 | `-` | unary `-` | Right
| | `+` | unary `+` | Right
| | `++` | unary increment |
| | `--` | unary decrement |
| | `all:` | set unary `all of` |
| | `any:` | set unary `any of` |
| | `none:` | set unary `none of` |
| | `!` | unary `not` |
| | `not` | unary `not` |
3 | `*` | multiplication | Left
| | `/` | division | Left
| | `^` | exponentiation | Left
| | `..` | range | --
| | `div` | integer division | Left
| | `mod` | modulo | Left
| | `mul` | integer multiplication | Left
4 | `+` | addition | Left
| | `-` | subtraction | Left
5 | `>` | greater-than | Left
| | `<` | less-than | Left
| | `<=` | less-than or equal-to | Left
| | `>=` | greater-than or equal-to | Left
6 | `==` | logical equality test | Left
| | `!=` | logical inequality test | Left
7 | `or` | logical `or` | Left
8 | `and` | logical `and` | Left
9 | `=` | assignment (non-mutating) | Right
| | `:=` | assignment (var) | --
| | `+=` | add and assign | -- 
| | `-=` | subtract and assign | --
| | `=>` | | Right
| | `->` | | Right
10 | `:` | key:value / declaration | ? (none)
11 | &#124; | chain | Left
| | `>>` | apply | Left
