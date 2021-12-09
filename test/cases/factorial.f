factorial(x) := {
    if x == 1 then
        return 1
    else
        return x * factorial(x - 1)
}

print(factorial(10))
