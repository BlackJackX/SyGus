from functools import reduce
from itertools import product
from z3 import *
from baseline.translator import toString


def constraint2clause(func, vars, constraints):
    """
    将constrain转化为逻辑语句
    :param func:
    :param vars:
    :param constraints:
    :return:
    """

    funcStr = '(declare-fun ' + func[1] + ' ('
    for var in func[2]:
        funcStr += var[1] + ' '
    funcStr += ') ' + func[-1] + ')'

    specSmt = [funcStr]
    for var in vars.items():
        if  isinstance(var[1], ArithRef) :
            specSmt.append('(declare-const %s Int)'%var[0])
        elif  isinstance(var[1], BoolRef) :
            specSmt.append('(declare-const %s Bool'%var[0])

    for constraint in constraints:
        specSmt.append('(assert %s)'%(toString(constraint[1:])))

    smtScript = reduce(lambda x, y:x + '\n' + y, specSmt)
    rawClause = parse_smt2_string(smtScript)


    return And(rawClause)

def raw2DNF(rawClause):
    """
    转化为dnf范式
    :param rawClause:
    :return:
    """
    rawClause = simplify(rawClause)
    clause = not_inward(rawClause)
    clause = distribute(clause)
    clause = check_clause_sat(clause)
    return clause

def not_inward(rawClause):
    """
    not移至最内层
    :param rawClause:
    :return:
    """
    rawClause = simplify(rawClause)
    if atom(rawClause):
        return rawClause
    op = rawClause.decl().name()
    children = rawClause.children()
    if op != 'not':
        children = list(map(lambda c: not_inward(c), children))
    else:
        inop = rawClause.children()[0].decl().name()
        inchildren = rawClause.children()[0].children()
        children = list(map(lambda c: not_inward(Not(c)), inchildren))
        op =  'and' if inop == 'or' else 'or'

    if op == 'and':
        return And(children)
    else:
        return Or(children)

def atom(clause):
    """
    若没有or和and则返回true
    :param clause:
    :return:
    """
    op = clause.decl().name()
    children = clause.children()

    if op == 'or' or op == 'and':
        return False
    elif op == 'not':
        return atom(children[0])

    return True

def distribute(clause):
    """
    若用and连接，则找到and子句中所有or，分配率
    若用or连接，则找到or子句中所有and内的or，处理，也就是对每个or子句用
    分配率
    :param clause:
    :return:
    """
    other_clauses = []
    or_clauses = []
    clause = simplify(clause)
    children = clause.children()
    op = clause.decl().name()

    if op == 'or':
        return Or(list(map(lambda c: distribute(c), children)))
    elif op == 'and':
        for c in children:
            if c.decl().name() == 'or':
                or_clauses.append(c.children())
            else:
                other_clauses.append(c)
        or_clauses = list(product(*or_clauses))
        clauses = []
        for oc in or_clauses:
            clauses.append(And(other_clauses+list(oc)))
        return Or(clauses)

    return clause

def check_clause_sat(clause):
    """
    检查每个子句是否sat，若不sat，则弃掉
    :param clause:
    :return:
    """
    children = clause.children()
    children = list(filter(lambda c: check_sat(c), children))
    return Or(children)


sat     = CheckSatResult(Z3_L_TRUE)
unsat   = CheckSatResult(Z3_L_FALSE)
unknown = CheckSatResult(Z3_L_UNDEF)

def check_sat(clause):
    s = Solver()
    s.add(clause)

    if s.check() == sat:
        return True
    else:
        return False


