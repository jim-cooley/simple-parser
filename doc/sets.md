# Thoughts on Sets

What's the difference between a Set and a Block?

| | Sets | Blocks
| --- | --- | ---
Contains literal values | Y | ? 
Contains keys | Y | Y
Can contain functions | N | Y
Keys can be complex | ? | Y
Keys can contain functions | N | Y
Keys can be identifiers | y | Y
Values can contain expressions | ? | Y
Expressions are re-evaluated after assignment (functions) | N | Y
Key / value separator | ':' | '=', ':='
Can be used as Datasets | Y | N
Can be parameterized | Y | Y
Work with any:, all:, none: | Y | Y

> Q: Are Datasets just Sets?
>
> A: Unsure, probably.  But Datasets are more R/C, so would make more sense to base upon 2D Lists