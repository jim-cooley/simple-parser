# list
a = 1..10
print("slicing list")
print(a[-1])
print(a[:-1])
print(a[3:])
print(a[1:10])
print(a[::2])
print(a[:10:2])
print(a[1:10:2])

# nd.array
1..10 | reshape(_, 2, 5) | flatten | a
print("slicing nd.array")
print(a[-1])
print(a[:-1])
print(a[3:])
print(a[1:10])
print(a[::2])
print(a[:10:2])
print(a[1:10:2])

d = { 'col1': [1, 2], 'col2': [3, 4] }
print(d)
