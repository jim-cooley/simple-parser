#
# Focal - Formulaic Calculator (ExCal - ?)
#
# Expression based
#
#
#   '=' for static evaluation - evaluates formula, stores result
#   ':=' for var evaluation - stores formuala, re-evaluates on get, like inline function
#   'def' + target + '=' is the same as target + ':='   # why 2 syntax?
#   ',' # separator for lists, tuples, sets, etc
#   ';' # statement separator, discards evaluation on lhs
#
#   expression + '|' + expression      - expression separator, chains evaluation from lhs to rhs
#                                      - '3 | a' should be the same as 'a = 3'
#                                      - but might be better expressed as '3 >> a'
#
#   expression + '>>' + target    # apply operator -- sets or stores lhs expression
#
#   set + ':' + set     - applies the rhs to the lhs set : modifies contents, parameterizes
#   set + ':' + tuple   - same
#
# what's the difference between set, tuple, and block?
#
#   block - contains statements and expressions
#   set - contains statements, and expressions, with k-v pairs (but could be anonymous?)
#
#   list, tuple - sequenctial, ordered, iterable, heterogeneous, allows duplicates, nestable
#   set - unordered, heterogeneous, no duplicates (coalesced), nestable
#   dictionary - k,v pairs
#
#   tuple = '(' + item + [',' + item]* + ')'                    tuple(), ()
#   list = '[' + item + [',' + item]* + ']'                     list(), []
#   set = '{' + item + [',' + item]* + ']'                      set()
#   dictionary = '{' + key:value + [',' + key:value]* + '}'     dict(), {}
#
#   indexing:
#   a[1]        - single value
#   a[0..10]    - range query
#   a[a > 10]   - select from a where a > 10
# can appear on lhs
#   a[a > 10] = 0
#
# row, col:
#   a['col']              - select col from a
#   a['col1', 'col2', 'col3'] - select col1, col2, col3 from a
#   a['col'][0]           - first row of select col from a
#   a[col] | top        - top from a[col]
#   a[col][10/31/2021]  - range for 10/31/2021 (all values that date)
#   a[col][1d]          - past 1d from a[col]
#   a[col='col', row='10/31/2021']  - alternate syntax
#   a[1d]               - when using duration, time, or integers, row is assumed if not specified
#   a[row=1d]           - formal syntax
#   a{1d}               - maybe use {} for row-based query?
#   a.col1              - alternate syntax
#   a.col1[1d]          - good for single column
#   a['col1', 'col2' > 0, 'col3']
#   a[col1:, col2:, col3: ]  - uses table metadata and bypasses string lookups
#   a[col1:, col2: > 10, col3: ]  - uses table metadata and bypasses string lookups
#
# sets: can contain formula, expressions
#   a := {
#       buy: close >| sma(10) | signal | delay(1d) >> atr
#       sell: close <| sma(10) | signal | delay(1d) >> atr
#   }
#
# some scala notation:
# (x: R) => x * x           - anonymous function
# (1 to 5).map(_ * 2)       - anonymous function
# (1 to 5).map(x => x * x)  - use of arg twice, must name
# (1 to 5).reduceLeft(_ + _) - use of unnamed args
#
# inline functions: re-evaluated each access
# def f(x) := { x * x } - define function
# def f(x) := println(x)
# def f(x) := x * x
# def f(x) := { a | b | c }:{threshold = x}
# f(x) := x * x             - alternate syntax
# f(x) = x * x              - ?
#
# more scala:
# (1 to 5) filter {
#    _ % 2 == 0
#  } map {
#    _ * 2
#  }
#
# focal equivalent:
# (1..5) | filter:{where: _ % 2 == 0} | map:{_ * 2}
# (1..5) | map:{_ % 2 == 0 => _ * 2}
# (1..5) | map[_ % 2 == 0] => _ * 2
# (1..5) | map[_ % 2 == 0] *= 2
# (1..5) | map:{ _ % 2 == 0 => _ * 2 }
#
# scala:
# val zscore =
#    (mean: R, sd: R) =>
#      (x: R) =>
#        (x - mean) / sd
# val normer = zscore(7, 0.4) _
#
# focal:
# zscore(mean:, sd:) = { (x - mean) / sd }
# normer = zscore(7,0.4)
#
# zscore(mean:, sd:) = { (x - mean) / sd }
# normer = zscore:{mean=7, sd=0.4}
# scores['score']:{zscore:(mean=7, sd=0.4)}      # apply to table 'scores'
# scores['score']:{zscore:(mean=7, sd=0.4)} | normalized_scores
# scores['score']:{normer} | normalized_scores
# scores['score']:{normer} >> normalized_scores
#
# variables
# var x = 5                 - mutable, denotes dimension of simulation
# x = 5                     - immutable
# var (x, y, z) = (1, 2, 3)
# (x, y, z) = (1, 2, 3)
#
# conditionals:
# happy if check
# happy if check else sad
# a = happy if check
# a = happy if check else sad
#
# implicit looping: (while-do)
# (x < 5) {
#   println(x)
#   x += 1
# }
#
# {                 (do-while)
#   println(x),
#   x += 1
# }:(x=0, x < 5)
#
# scala:
# (xs zip ys) map {
#    case (x, y) => x * y
#  }
#
# for (x <- xs; y <- ys)
#    yield x * y
#
# (i <- 1 to 5) {
#    println(i)
#  }
#
# val v42 = 42
#  3 match {
#    case `v42` => println("42")
#    case _     => println("Not 42")
#  }
#
# python:
#   a_list = [1, ‘4’, 9, ‘a’, 0, 4]
#
#   squared_ints = [ e**2 for e in a_list if type(e) == types.IntType ]
#
# filter(lambda e: type(e) == types.IntType, a_list)
# map(lambda e: e**2, a_list)
# map(lambda e: e**2, filter(lambda e: type(e) == types.IntType, a_list))
# [ [ 1 if item_idx == row_idx else 0 for item_idx in range(0, 3) ] for row_idx in range(0, 3) ]
# multiples = [i for i in range(30) if i % 3 == 0]
# squared = [x**2 for x in range(10)]
#
#
# mcase = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}
#
# mcase_frequency = {
#    k.lower(): mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0)
#    for k in mcase.keys()
# }
# >> mcase_frequency == {'a': 17, 'z': 3, 'b': 34}
#
#   {v: k for k, v in some_dict.items()}
#
# python generator:
# multiples_gen = (i for i in range(30) if i % 3 == 0)
# print(multiples_gen)
# Output: <generator object <genexpr> at 0x7fdaa8e407d8>
# for x in multiples_gen:
#   print(x)
#
# python lambdas:
# lambda argument: manipulate(argument)
# add = lambda x, y: x + y
# a = [(1, 2), (4, 1), (9, 10), (13, -3)]
# a.sort(key=lambda x: x[1])
#
# data = zip(list1, list2)
#  data = sorted(data)
#  list1, list2 = map(lambda t: list(t), zip(*data))
#
# python ternary:
# (if_test_is_false, if_test_is_true)[test]
# nice = True
# personality = ("mean", "nice")[nice]
# print("The cat is ", personality)
#
# output = None
# message = output or "no input received"
#
# Output: The cat is nice
#
# Python ternary 'tag'
# True or "Some"
# False or "Some"
#
# in a flow:
#   a[a > 10] = 0 | b   - lhs is propigated by '|'.  similar to '=' but left to right evaluation
#   a = b = c           - c is assigned to b, is assigned to a
#   a | b | c           - a is assigned to b, is assigned to c
#
# pandas formulae:
#   a | rolling(window=n) | mean
#   a | rolling:{window=n} | mean
#   { a | rolling | mean}:(window=n)
#
# implicit looping:
#   n = [0..10]
#   { a | rolling | mean}:(window=n)
#   - evaluates for n=0..10
#
#expression :=   literal
                | unary
                | binary
                | assignment
                | fn_call
                | '(' + expression + ')'
                | expression + ';' + expression
                | expression + '|' + expression
                | expression + '>>' + target
                | '{' + expression + [ ';', ',', '|' ] expression + '}'

assignment := ['def' | 'var'] + target + ['=' | ':='] + expression

tuple := '(' + expression + [',' + expression ]* + ')'

parameter_list := '(' + expression + [',' + expression ]* + ')'

term := factor [[ '-' | '+' ] factor ]*

factor := unary [[ '/' | '*' | 'div' | 'mod' ] factor ]*

unary := [ '-' | '!' | 'not' ] unary
         | primary

primary :=  number | datetime | duration | set | STRING | 'true' | 'false' | 'none'
            | '(' expression ')'

