a=1; b=0; a |> b

# apply
a >> b
1 >> 2
1 >> -1
1 >> false
2 >> none
3 >> empty
false >> 2
false >> true
false >> false
false >> none
false >> empty
true >> 2
true >> true
true >> false
true >> none
true >> empty
none >> 2
none >> true
none >> false
none >> none
none >> empty
empty >> 2
# rise above:
a |> b
1 |> 2
1 |> -1
1 |> false
2 |> none
3 |> empty
false |> 2
false |> true
false |> false
false |> none
false |> empty
true |> 2
true |> true
true |> false
true |> none
true |> empty
none |> 2
none |> true
none |> false
none |> none
none |> empty
empty |> 2
# fall below:
a <| b
1 <| 2
1 <| -1
1 <| false
2 <| none
3 <| empty
false <| 2
false <| true
false <| false
false <| none
false <| empty
true <| 2
true <| true
true <| false
true <| none
true <| empty
none <| 2
none <| true
none <| false
none <| none
none <| empty
empty <| 2
# addition
a + b
1 + 2
1 + -1
1 + false
2 + none
3 + empty
false + 2
false + true
false + false
false + none
false + empty
true + 2
true + true
true + false
true + none
true + empty
none + 2
none + true
none + false
none + none
none + empty
empty + 2
# subtraction
a - b
1 - 2
1 - -1
1 - false
2 - none
3 - empty
false - 2
false - true
false - false
false - none
false - empty
true - 2
true - true
true - false
true - none
true - empty
none - 2
none - true
none - false
none - none
none - empty
empty - 2
# multiplication
a * b
1 * 2
1 * -1
1 * false
2 * none
3 * empty
false * 2
false * true
false * false
false * none
false * empty
true * 2
true * true
true * false
true * none
true * empty
none * 2
none * true
none * false
none * none
none * empty
empty * 2
# division
a / b
1 / 2
1 / -1
#1 / false - div by zero
2 / none
3 / empty
false / 2
false / true
true / 2
true / none
true / empty
none / 2
none / empty
empty / 2
# exponentiation
a ^ b
1 ^ 2
1 ^ -1
1 ^ false
2 ^ none
3 ^ empty
false ^ 2
false ^ true
false ^ false
false ^ none
false ^ empty
true ^ 2
true ^ true
true ^ false
true ^ none
true ^ empty
none ^ 2
none ^ true
none ^ false
none ^ none
none ^ empty
empty ^ 2
# assignment
a = b
