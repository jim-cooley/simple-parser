#
# a 'sniff-test' composed of grammatical edge cases among the parser states
#

# prime:
#   NUMBER | DATETIME | DURATION | SET | STRING | true | false | none

# declaration:
#   _statement_
#   'def' _var_declaration_
#   'var' _definition_
#   '%%' _command
var f = 5
var f = x
var f(x) = x * 4
var f.a.b.c = 5
var f.a.b.c(x) = x*x # vars in parameter list need to be Ref, not Get's
var (a, b, c) = (4, 5, 6)

def f = 5
def f = x
def f(x) = x * 4
def f.a.b.c = 5
def f.a.b.c(x) = x*x # vars in parameter list need to be Ref, not Get's
def (a, b, c) = (4, 5, 6)

f = 5
f = x
f(x) = x * 4
f.a.b.c = 5
f.a.b.c(x) = x*x # vars in parameter list need to be Ref, not Get's
(a, b, c) = (4, 5, 6)

# statement:
#   _expression_
#   { _block_ }
#   { _block_ }:( _tuple_ )
#   { _block_ }:{ _block_ }
#   _statement_ ; _statement_
a; b; c
{ b };
{ a(x):x*x }
f := { a(x):x*x }; { b: b.left = b.right}:(node);
var f = { a(x):x*x }
def f = { a(x):x*x }
f := { a(x):x*x }
{ b: b.left = b.right}:(node)


# expression:
#   _assignment_
#   _assignment_ | _assignment_
#   _assignment_ => _assignment_
#   _assignment_ >> _assignment_
#   _assignment_ -> _assignment_
a | b | c >> d
{ b => b.left = b.right}:(node)
{ _ => _.left = _.right}:(node)
{ b } => buy
