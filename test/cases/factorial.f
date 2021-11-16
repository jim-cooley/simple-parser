def factorial(x) := {
    print('in factorial')
    if x == 1 then
        return 1
    else
        return x * factorial(x - 1)
}

result = factorial(5)
print(result)

