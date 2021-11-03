
{ b } => buy
any:{a, b, c}
any:{a=False, b=False, c=False}:(a=True)
any:{a=False, b=False, c=False}:{a=True}
{ b : b.left = b.right}:(node)
{ _ : _.left = _.right}:(node)

node => { b : b.left = b.right}
node => { _ : _.left = _.right}

# { b }:{node} := {b.left = b.right}
{ b }:{node} => {b.left = b.right}
node | { _ : _.left = _.right}
{ b } | buy
{ b } >> buy
{ b } => buy
a,
( b ) | buy
