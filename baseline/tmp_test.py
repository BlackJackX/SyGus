from baseline.transform import *
from z3 import *
f = Function('f', IntSort(), IntSort())
x = Int('x')
y = Int('y')
z = Int('z')

print(list(filter(has_func, [['=', 'x', ['max3', 'x', 'y', 'z']]])))