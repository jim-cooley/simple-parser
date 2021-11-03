var f = { a:5 }
var f = { a=5 }
var f.a.b.c(x) = x*x
var f = 5
var f.a = 5
var f.a.b.c = 5

var f = { a(x):x*x }
var f = { a(_):_*_ }
var f = { 5 }
var f := 5
var f := { 5 }
var f(x) := x * 4;
var f(x) = x * 4
var f(x) = { a(x):x*x }

# def declarations
def f(x) := x * 4;
def f(x) = x * 4
def f(x) := { x * 4 }
def f(x) = { a(x):x*x }
def f(x) = { a.b(x):x*x }

# unspecified
f(x) := x * 4;
f(x) = x * 4
f(x) := { x * 4 }
f(x) = { a(x):x*x }
f = { a(x):x*x }
