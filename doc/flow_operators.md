# Flows

Flows are a series of transforms applied to a datasource that ultimately wind up producing or storing something.  If you are familiar with Shell scripting, then a flow is very similar to a series of 'pipe' expressions and the i/o redirect operator '>>'.  In Focal, flows consist of a `source`, a series of `transforms`, and a `destination`.  

### Source
The source may be a literal value, a dataset or other variable, or a function that produces an output.

### Transforms, Transform Functions
Transforms are operations that are applied to the results of the previous expression and in the case of sets, may be applied either element-wise or to the set as a whole.

### Destination
A Flow destination may be a variable, event, or function that produces an output.

## Flow Operators

Flow operators are '|', '=>', and '>>'.  Here is how they differ:

operator | name | description
:---: | --- | ---
&#124; | `chain` or `pipe` | Connects transform functions together, producing a flow of data through various transformations 
`>>` | `apply` | Assigns the product of a series of flow transitions to storage.  Example: `a >> b`, would be equivalent to `b` = `a`
`=>` | `produce` or `yield` |  Used as a pattern substitution / ananymous function declaration.  Example: `x => x + 1` would apply the anonymous function `x + 1`, where `x` occurred.  In this case, `x` is an anonymous variable and its name does not matter.  The expression could also be written: ` _ => _ + 1`
`->` | `raise` | Used to raise a signal or invoke a function for each non-zero value in the dataset.  Raise is similar to `apply` in that it could send the output to variable or dataset, but unlike `apply`, values would aggretate in the destination.

## Valid Forms

### Flow / Chain (&#124;)
The Flow or Chain operator is used to connect transform functions together into a dataflow.

Example | Discussion
--- | ---
`passengers` &#124; `bin('auto,k=10,column='age')` &#124; `countby('age_bin1')` &#124; `sortby('age_bin1')` | general form
`passengers` &#124; `bin:{'type='auto', k=10, column='age'}` &#124; `countby:{'age_bin1'}` &#124; `sortby:{'age_bin1'}` | alternate parameterization
`{ passengers` &#124; `bin` &#124; `countby(_)` &#124; `sortby(_)}:{'type='auto', k=10, column='age'}` | flow parameterization
{`passengers` &#124; `bin` &#124; `countby` &#124; `sortby }:{'type='auto', k=10, column='age'}` | removal of nonessential anonoymous parameters



### Apply (>>)
The Apply operator is a right to left assignment operator.  Think of it as the inverse of `=`.
Here are some examples:

Example | Assignment | Discussion
--- | --- | ---
`5 >> a` | `a = 5` | standard assignment form
`a + 1 >> a` | `a = a + 1`, `a += 1` |
`{dataset}` &#124; `select(column='value') >> a` | `a = select from dataset where column='value'` | flow production form




### Produce (=>)
The following are all valid forms of the declaration of an anonymous production function:

Example | Discussion
--- | ---
`x: x + 1` | formal notation
`x => x + 1` | product notation
`_ => _ + 1` | anonymous product notation
`f(x): x + 1` | function notation
`f(x) => x + 1` | product function notation
`f(_) => _ + 1` | anonymous product fuction notation
`f(x) = x + 1` | function assignment notation (non mutating?)
`f(x) := x + 1` | function definition notation (mutating, inline function)

Additionally, these may appear with or without block / set notation `{`..`}` or expression grouping `(`..`)`, as in the following examples

Example | Discussion
--- | ---
`{ x: x + 1 }` | formal notation
`( x => x + 1 )` | product notation
`( _ => _ + 1 )` | anonymous product notation
`f(x): { x + 1 }` | function notation
`f(x) => ( x + 1 )` | product function notation
`f(_) => { _ + 1 }` | anonymous product fuction notation
`f(x) = { x + 1 }` | function assignment notation (non mutating?)
`f(x) := ( x + 1 )` | function definition notation (mutating, inline function)



