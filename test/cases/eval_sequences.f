%%option{strict=false}
a | { b:1 } | c
a | { b=1, 'k':v } | c
a | { b + 1 } | c
a | { b => b + 1 } | c
a = 4
a | ( b : b + 1 ) | c
a | { b => b + 1 } | c

a = 5
4 | b
4 >> b
4 => b
# a | b: b + 1 | c
a | b + 1 | c
a | _ + 1 | c
3 | _ + 1 | c

a | b | c
a >> b
a | b >> c
a | b | c => d
a | b => c | d
a | { b + 1 } | c
