x = 5
print(x)

dates = range('1/1/2020', 5)
df = {reshape(1..24, 6,4), index=dates}
print(df)

df = {random(6, 4), columns=['A','B','C','D'], index=dates}
print(df)

# datasets:
x = range('1/1/2000', periods=1000)
print(series(x))

pd = dataset()

d = {'col1': [1, 2], 'col2': [3, 4]}
print(d)

df = {
    one: integers(1..10, 4), index=["a", "b", "c", "d"],
    two: integers(1..10, 4), index=["a", "b", "c", "d"],
    three: integers(1..10, 4), index=["a", "b", "c", "d"],
    four: integers(1..10, 4), index=["a", "b", "c", "d"],
}
print(df)

df = {
    'one': 1..4,
    'two': 2..5,
    'three': 3..6,
    index=["a", "b", "c", "d"],
}
print(df)

# from pandas docs:
df = {
    "one": random(4),
    "two": random(4),
    "three": random(4),
}
print(df)

# future definition with generators?
#df = {
#    "one": { random(3) => _ },
#     index=['a', 'b', 'c']
#}

sugar(x) = { x + 1 }

def simple(x) := {
    x + 1
}

def simple(x) := {
    x = 1
}

def factorial(x) := {
    if x == 1 then
        return 1
    else
        return x * factorial(x - 1)
}

dates = range('1/1/2020', 5)
df = {random(6, 4), columns=['A','B','C','D'], index=dates}
print(df)

df = {reshape(1..24, 6,4), index=dates}
print(df)

df = {
    one: 1..4,
    two: 2..5,
    three: 3..6,
    four: 4..7,
    index=["a", "b", "c", "d"],
}
print(df[-1])

print(factorial(10))

1..24 | reshape(_, 6,4) | dataframe >> Z | print

print(type(Z))

