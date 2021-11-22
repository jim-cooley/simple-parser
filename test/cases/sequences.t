# tuple
(1, 2, 3)   # List(TK.TUPLE)

# named tuple: (tuple list)
(x:1, y:2, z:3)  # List(TK.TUPLE: Define(TK.COMBINE), Define(TK.COMBINE), Define(TK.COMBINE))
(x=1, y=2, z=3)  # List(TK.TUPLE: Define(TK.DEFINE), Define(TK.DEFINE), Define(TK.DEFINE))

# set with named values
{a:4, b:3, c:2}

# tuple assignment
(x, y, z) = (1, 2, 3) # Define(TK.DEFINE: List(TK.TUPLE) '=' List(TK.TUPLE))

# simple assignment with parameterization
a = {q, r, s}:(1, 2, 3)

# tuple assignment with parameterization
(x, y, z) = {q, r, s}:(1, 2, 3) # Define(TK.DEFINE: List(TK.TUPLE: Ref, Ref, Ref) '=' Combine( Set(Ref, Ref, Ref) ':' List(TK.TUPLE: Lit, Lit, Lit) ) )

#
(x, y, z) = {q, r, s}:[1, 2, 3] #

# tuple assignment with keyword parameterization
(x, y, z) = {q, r, s}:{q=1, s=3, r=2}   # Define(TK.DEFINE: List(TK.TUPLE: Ref, Ref, Ref) '=' Combine( Set ':' List(TK.TUPLE: Define, Define, Define)  ) # NamedTuple() ?

{a}:(threshold=0.05, how='any')
[1..10 => b: b * 2]
[1..100] => { _ : _ ^ 2}
{a, b, c}:(4, 5, 6)
any:{a, b, c}
{a, b, c}:(c=4, a=5, b=6)
any:{a=False, b=False, c=False}:(a=True)
var f = { a=5 }
[1..100]:{step=5}

[1..100]
[1..100]:5
[range(0,100)]

[b => b + 1 in (1..100)]
{x=1, y=2, z=3*(x+y)}
{x=1, y=2, z=3*(x+y)}:(x=1, y=2, z=3)
def c = {x=1, y=2, z=3*(x+y)}:(x=1, y=2, z=3)

(x, y, z) = (1, 2, 3)
(x, y, z) = {q, r, s}:(1, 2, 3)
(x, y, z) = {q, r, s}:{q=1, r=2, s=3}
a = (1, 2, 3)
a = {q, r, s}:(1, 2, 3)
a = {q, r, s}:{q=1, r=2, s=3}

