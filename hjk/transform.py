from functools import reduce
from itertools import product
from z3 import *
from hjk.translator import toString
from copy import deepcopy

oplist = ['<', '>', '>=', '<=', '=', 'or', 'and', '+', '-']


class Clause():
    def __init__(self):
        self.defDom = []
        self.valDom = []

    @classmethod
    def constraint2clause(cls, constraint):
        op = constraint[0]
        clause = Clause()
        if op == 'or':
            clause.defDom.append(rev(['or'] + constraint[1:-1])[1:])
            clause.valDom.append(constraint[-1][-1][1])
        else:
            clause.defDom.append(constraint[1:-1])
            clause.valDom.append(constraint[-1][1])
        return clause

    @classmethod
    def clauses_union(cls, clauses):
        clause = Clause()
        for c in clauses:
            clause.defDom.extend(c.defDom)
            clause.valDom.extend(c.valDom)
        return clause

    def clause2prog(self):
        return self.valdef2str(self.defDom, self.valDom)


    @staticmethod
    def defDom2str(defDom):
        s = ''
        if len(defDom) == 1:
            return '(%s %s %s) ' %tuple(defDom[0])
        s += '(and '
        s += '(%s %s %s) ' %tuple(defDom[0])
        s += Clause.defDom2str(defDom[1:])
        s += ')'
        return s

    @staticmethod
    def valdef2str(defDom, valDom):
        s = ''
        if len(valDom) == 1:
            return '(ite %s %s 0)' %(Clause.defDom2str(defDom[0]), valDom[0])
        s += '(ite '
        s += '%s %s ' %(Clause.defDom2str(defDom[0]), valDom[0])
        s += Clause.valdef2str(defDom[1:], valDom[1:])
        s += ')'
        return s


def rev(constraints):
    op = constraints[0]
    cs = constraints[1:]
    if op == '>=':
        return ['<', *cs]
    elif op == '<=':
        return ['>', *cs]
    elif op == '<':
        return ['>=', *cs]
    elif op == '>':
        return ['<=', *cs]
    elif op == 'or':
        return ['and', *list(map(rev, cs))]
    elif op == 'and':
        return ['or', *list(map(rev, cs))]
    else:
        return []

def implies2or(constraints):
    '''
    =>转or
    '''
    if not isinstance(constraints, list):
        return constraints
    op = constraints[0]
    cs = constraints[1:]
    if op == '=>':
        return ['or', rev(implies2or(cs[0])), implies2or(cs[1])]
    else:
        return [op, *list(map(implies2or, cs))]


def logic_simplify(constraints):
    if not isinstance(constraints, list):
        return constraints
    op = constraints[0]
    if op not in ['and', 'or']:
        return constraints
    cs = constraints[1:]
    cs = list(map(logic_simplify, cs))
    newCs = [op]
    for c in cs:
        if isinstance(c, list) and c[0] == op:
            newCs.extend(c[1:])
        else:
            newCs.append(c)

    return newCs


def div_func(constraints):
    """
    对于max将or分配，并换元
    对于array_search，不动
    """
    if constraints[1][0] == 'or':
        return constraints
    or_cs = constraints[-1][1:]
    other_cs = constraints[1:-1]

    return ['or'] + list(map(lambda x: ['and', *deepcopy(other_cs), x], or_cs))



def change_var(constraints):
    """
    假设此时每个constrains只有一个f=a
    """
    if constraints[0] == 'and':
        return constraints

    for c in constraints[1:]:
        val = c[-1][1]
        for in_c in c[1:-1]:
            in_c[1] = val

    return constraints

def pipline(constraints):
    '''
    从constraint的list生成program
    1. 形成一个constraint
    2. 将=>转化成or
        此时应该是 （And (Or x x) (Or x x) ....)
    3. 若Or中有多个f，分配开
    4. 对And中每个子句进行换元，删除不合法子句
    5. 把And中每个list生成clause
    6. clauses合并成一个clause
    7. 从clause生成程序
    '''

    cs = ['and']
    constraints = list(map(lambda c: c[1], constraints))
    cs.extend(constraints)
    cs = implies2or(cs)
    cs = logic_simplify(cs)
    cs = div_func(cs)
    cs = change_var(cs)

    clauses = []

    for c in cs[1:]:
        clauses.append(Clause.constraint2clause(c))

    clause = Clause.clauses_union(clauses)
    program = clause.clause2prog()

    return program
