from baseline.transform import *
from z3 import *
f = Function('f', IntSort(), IntSort())
x = Int('x')
y = Int('y')
z = Int('z')

print(Clause.valdef2str([
[['>=', 'x', 'x'], ['>=', 'x', 'y'], ['>=', 'x', 'z']],
[['>=', 'y', 'x'], ['>=', 'y', 'y'], ['>=', 'y', 'z']],
[['>=', 'z', 'x'], ['>=', 'z', 'y'], ['>=', 'z', 'z']]
],
['x', 'y', 'z'] ))


(define-fun max10 ((x1 Int)(x2 Int)(x3 Int)(x4 Int)(x5 Int)(x6 Int)(x7 Int)(x8 Int)(x9 Int)(x10 Int)) Int (ite (and (>= x1 x1) (and (>= x1 x2) (and (>= x1 x3) (and (>= x1 x4) (and (>= x1 x5) (and (>= x1 x6) (and (>= x1 x7) (and (>= x1 x8) (and (>= x1 x9) (>= x1 x10) ))))))))) x1 (ite (and (>= x2 x1) (and (>= x2 x2) (and (>= x2 x3) (and (>= x2 x4) (and (>= x2 x5) (and (>= x2 x6) (and (>= x2 x7) (and (>= x2 x8) (and (>= x2 x9) (>= x2 x10) ))))))))) x2 (ite (and (>= x3 x1) (and (>= x3 x2) (and (>= x3 x3) (and (>= x3 x4) (and (>= x3 x5) (and (>= x3 x6) (and (>= x3 x7) (and (>= x3 x8) (and (>= x3 x9) (>= x3 x10) ))))))))) x3 (ite (and (>= x4 x1) (and (>= x4 x2) (and (>= x4 x3) (and (>= x4 x4) (and (>= x4 x5) (and (>= x4 x6) (and (>= x4 x7) (and (>= x4 x8) (and (>= x4 x9) (>= x4 x10) ))))))))) x4 (ite (and (>= x5 x1) (and (>= x5 x2) (and (>= x5 x3) (and (>= x5 x4) (and (>= x5 x5) (and (>= x5 x6) (and (>= x5 x7) (and (>= x5 x8) (and (>= x5 x9) (>= x5 x10) ))))))))) x5 (ite (and (>= x6 x1) (and (>= x6 x2) (and (>= x6 x3) (and (>= x6 x4) (and (>= x6 x5) (and (>= x6 x6) (and (>= x6 x7) (and (>= x6 x8) (and (>= x6 x9) (>= x6 x10) ))))))))) x6 (ite (and (>= x7 x1) (and (>= x7 x2) (and (>= x7 x3) (and (>= x7 x4) (and (>= x7 x5) (and (>= x7 x6) (and (>= x7 x7) (and (>= x7 x8) (and (>= x7 x9) (>= x7 x10) ))))))))) x7 (ite (and (>= x8 x1) (and (>= x8 x2) (and (>= x8 x3) (and (>= x8 x4) (and (>= x8 x5) (and (>= x8 x6) (and (>= x8 x7) (and (>= x8 x8) (and (>= x8 x9) (>= x8 x10) ))))))))) x8 (ite (and (>= x9 x1) (and (>= x9 x2) (and (>= x9 x3) (and (>= x9 x4) (and (>= x9 x5) (and (>= x9 x6) (and (>= x9 x7) (and (>= x9 x8) (and (>= x9 x9) (>= x9 x10) ))))))))) x9 (ite (and (>= x10 x1) (and (>= x10 x2) (and (>= x10 x3) (and (>= x10 x4) (and (>= x10 x5) (and (>= x10 x6) (and (>= x10 x7) (and (>= x10 x8) (and (>= x10 x9) (>= x10 x10) ))))))))) x1 0)))))))))))