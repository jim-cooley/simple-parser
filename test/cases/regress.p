f(x) = x*x

def factorial(x) := {
    if x == 1 then
        return 1
    else
        return x * factorial(x - 1)
}

print('hello')
f(5)
# factorial(5)

