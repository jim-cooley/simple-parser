a = [1, 2, 3]
b = [4, 5, 6]

x = eye(5)
1..25 | reshape(_, 5,5) | y
print(x)
print(y)
print(x * y)

c = a * b

print (c)
print(c ^ 2)
print(c * 3)
print(c + 1)

b = [[1,2,3],[4,5,6],[7,8,9]]
print(b)
print(b ^ 2)
print(b * 2)
print(b - 2)
print(b / 2)
# print(b // 2)

c = zeros(2)
print(c)
c = zeros(2,2)
print(c)
c = ones(2,2)
print(c)
c = eye(5,5)
print(c)
d = ones(5,5)
print(c * d * 2)


def factorial(x) := {
    print('in factorial')
    if x == 1 then
        return 1
    else
        return x * factorial(x - 1)
}

result = factorial(5)
print(result)

a = [1..10]
print(a)

s1 = [name:'series', 'a':5, 'b':'c', 'd'=3, index=['a','b']]
# s = ['series':[5, 6, 7, 8, 9, 10], name:'series', index=['series']]

def fn(x, y) = x*y
r = fn(2, y=3)

#s = [5, 6, 7, 8, 9, 10, name:'series']
print(a)
print(s1)
print(s)
