def simple(x) := {
    x + 1
}

def factorial(x) := {
    x * factorial(x - 1)
}

sugar(x) => { x + 1 }
