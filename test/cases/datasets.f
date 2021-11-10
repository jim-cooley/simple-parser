# datasets:
pd = dataset()

df = {
    "one": Series( rand(3) ) : { index=["a", "b", "c"] },

    "two": Series( rand(4) ) : index=["a", "b", "c", "d"],

    "three": Series( rand(3), index=["b", "c", "d"] ),
}

# would be nice if df was already a dataframe from the decl above.
pd = dataset(df)

# future definition with generators?
df = {
    "one": { rand(3) => _ } : index=['a', 'b', 'c']
}
