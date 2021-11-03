(a)                          # grouping
f(a)                         # parameter list (tuple)
(a) = 5                      # grouping
(a) = (5)                    # grouping or tuple assignment?
(a,)                         # tuple
(a, b)                       # tuple
f(a,b)                       # parameter list (tuple)
((a))                        # grouping
(2 + 4) * 3                  # expression grouping
((2 + 4) * 3)                # expression grouping
((a,))                       # grouping of tuple
((a,),)                      # tuple in a tuple
((a), b)                     # grouping in tuple
((a, b))                     # grouping of tuple
((a, b), c)                  # tuple in a tuple
((a, b), (c))                # tuple in a tuple with grouping
(((a), (b)), (c))            # tuple in a tuple with more grouping
(a, b, c,)                   # tuple
(a, b, c) = (4, 5, 6)        # tuple assignment
(a, b, c) := (4, 5, 6)       # tuple assignment (var)
(a, b, c) = (a:5, b:3, c:4)  # tuple assignment k:v
{a, b, c}:(4, 5, 6)          # set parameterization
{a, b, c}:(a:5, b:3, c:4)    # set parameterization k:v
{a, b, c}:(a=5, b=3, c=4)    # set parameterization k=v (error?)
{a, b, c}:{a=5, b=3, c=4}    # set parameterization k=v (block)
{a, b, c}:{a:5, b:3, c:4}    # set parameterization k=v (block)

