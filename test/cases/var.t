var f(x) = { var a.b(x):x*x }

f(x) = { var a(x):x*x }
f.a(x) = { var a(x):x*x }

var f = { var a(x):x*x }

var f(x) = { var a(x):x*x }
var f(x) = { var a.b(x):x*x }

f = { var a(x):x*x }
f.a = { var a(x):x*x }
f.a.b = { var a(x):x*x }

var f = { a(_):_*_ }

var f(x) = { a(_):_*_ }

f = { a(_):_*_ }

f(x) = { a(_):_*_ }


var f = { a(x):x*x }
f = { a(x):x*x }

var f = { a:5 }      # should be block, not set
f = { a:5 }      # should be block, not set

var f = { a=5 }      # should be block, not set
f = { a=5 }      # should be block, not set

var f.a.b.c(x) = x*x # vars in parameter list need to be Ref, not Get's
f.a.b.c(x) = x*x # vars in parameter list need to be Ref, not Get's

var f = 5
f = 5

var f.a = 5
f.a = 5

var f.a.b.c = 5
f.a.b.c = 5

var f = { a(x):x*x }
f = { a(x):x*x }

var f = { var a(x):x*x }
f = { var a(x):x*x }

var f = { a(_):_*_ }
f = { a(_):_*_ }

var f = { 5 }
f = { 5 }

var f := 5
f := 5

var f := { 5 }
f := { 5 }

var f(x) := x * 4;
f(x) := x * 4;

var f(x) = x * 4
f(x) = x * 4

var f(x) = { a(x):x*x }
f(x) = { a(x):x*x }
