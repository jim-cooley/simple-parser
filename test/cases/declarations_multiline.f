# var declarations
var f = 5
var f.a = 5
var f = { a=5 }
var f = { a(x):x*x }
var f = { a(_):_*_ }
var f = { 5 }
var f := 5
var f := { 5 }

# def declarations
def f(x) := x * 4;
def f(x) = x * 4
def f(x) := { x * 4 }
def f(x) := {
    x = 4
    y = 7
    x * y
}

# tuples
(x, y, z)
(1, 2, 3)
(x:1, y:2, z:3)
(x=1, y=2, z=3)
(x, y, z) = (1, 2, 3)
(x, y, z) = {q, r, s}:(1, 2, 3)
(x, y, z) = {q, r, s}:{q=1, r=2, s=3}
a = (1, 2, 3)
a = {q, r, s}:(1, 2, 3)
a = {q, r, s}:{q=1, r=2, s=3}

# blocks
{x, y, z}
{1, 2, 3}
{x:1, y:2, z:3}
{x=1, y=2, z=3}
{x=1, y=2, z=3*(x+y)}

{x, y, z}
{1, 2, 3}
{x:1, y:2, z:3}
{x=1, y=2, z=3}
{x=1, y=2, z=3*(x+y)}:(x=1, y=2, z=3)

# declarations 2
a = (x, y, z)
a = (1, 2, 3)
a = (x:1, y:2, z:3)
a = (x=1, y=2, z=3)

b := {x, y, z}
b := {1, 2, 3}
b := {x:1, y:2, z:3}
b := {x=1, y=2, z=3}
b := {x=1, y=2, z=3*(x+y)}

def c = {x, y, z}
def c = {1, 2, 3}
def c = {x:1, y:2, z:3}
def c = {x=1, y=2, z=3}
def c = {x=1, y=2, z=3*(x+y)}:(x=1, y=2, z=3)

var c = {x, y, z}
var c = {1, 2, 3}
var c = {x:1, y:2, z:3}
var c = {x=1, y=2, z=3}
var c = {x=1, y=2, z=3*(x+y)}:(x=1, y=2, z=3)


