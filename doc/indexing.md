# indexing

Examples of Indexing in Focal

expression | description
---------- | ------------
```a[1]``` | single value
```a[0..10]``` | range query
```a[a > 10]``` | select from a where a > 10

> ```a[a > 10] = 0``` can appear on lhs of an expression
