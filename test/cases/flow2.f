1..10 | reshape(_, 2,5) | print

# need to make parser EOL sensitive.  identifier + ( => fn call otherwise
1..10 | x | reshape(x, 2, 5) | y

ones(5,5) | flatten | reshape(_, 5, 5) | print

integers(1..10, 25) | reshape(_, 5, 5) | print
ones(5,5) | print
print(y)
(x, y) | print

4 | print
y = 5
4 | x | print
eye(5) | x | print

pd = dataset(x)
print(pd)

eye(5) | dataset(_) | print


df = {
    "one": Series( rand(3) ) : { index=["a", "b", "c"] },

    "two": Series( rand(4) ) : index=["a", "b", "c", "d"],

    "three": Series( rand(3), index=["b", "c", "d"] ),
}

# would be nice if df was already a dataframe from the decl above.
pd = dataset(df)
print(pd)
