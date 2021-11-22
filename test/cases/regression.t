{{a, b, c}}
{{1, 2, 3}}

f = { a=5 }      # should be block, not set
{1, 2, 3}
{a:1, b:2, c:3}

[a:5, b:4]
[a=5, b='c', d]

[1..10 => b: b * 2]
[1..100] => { _ : _ ^ 2}
[] * range(0,100)
[] * [1..10]
[1,2,3] * [4,5,6]
node => { _ : _.left = _.right}

[name='series']
[name:'series', 'a':5, 'b':'c', d, index=['a','b']]
[name:'series', 5, 6, 7, 8, 9, 10, index=['series']]
['a':5, 'b':'c', d]

# pd = dataset()
t = today
n = now
pd = yahoo( symbols='portfolio.csv', span=-5y )
#
