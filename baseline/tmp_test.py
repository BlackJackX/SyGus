from baseline.DNF import *
from z3 import *
f = Function('f', IntSort(), IntSort())
x = Int('x')
p = Bool('p')
q = Bool('q')
r = Bool('r')

print(deep_simplify(Or(And(p,And(q,And(q,And(x>2))),Or(r,q)))))
