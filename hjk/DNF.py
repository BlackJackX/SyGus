from functools import reduce
from itertools import product
from z3 import *
from hjk.translator import toString


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
    # TODO: 简化和check_sat效率都有问题
    rawClause = simplify(rawClause)
    clause = not_inward(rawClause)
    clause = distribute(clause)
    #clause = deep_simplify(clause)
    #clause = check_clause_sat(clause)

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
    # TODO: 先删除没有f的子句和f冲突的子句，再checksat
    children = clause.children()
    children = list(filter(lambda c: check_sat(c), children))
    return Or(children)


sat     = CheckSatResult(Z3_L_TRUE)
unsat   = CheckSatResult(Z3_L_FALSE)
unknown = CheckSatResult(Z3_L_UNDEF)

def check_sat(clause):
    """
    检查单个字句是否sat
    :param clause:
    :return:
    """
    s = Solver()
    s.add(clause)

    if s.check() == sat:
        return True
    else:
        return False

# 废弃
def deep_simplify(clause, **kwargs):
    """
    深度简化逻辑语句
    :param clause:
    :return:
    """

    if clause.children() == [] or (clause.decl().name() != 'and' and \
        clause.decl().name() != 'or' and clause.decl().name() != 'not'):
        return clause
    op = clause.decl().name()
    children = clause.children()
    children = list(map(lambda c: deep_simplify(c, **kwargs), children))

    if op == 'and':
        return simplify(And(children))
    elif op == 'or':
        return simplify(Or(children))
    else:
        return simplify(Not(children[0]))


# TODO: 把函数参数提出来当定义域
def func_transform(clause, func, num):
    op = clause.decl().name()
    if op not in ['or', 'and', 'not']:
        return clause
    children = []

    for c in clause.children():
        if c.children() != []:
            children.append(clause)
        elif c.arg(0).decl() == func:
            print('111')
            func_op = c.decl()
            tmp_children = []
            new_var = []
            for arg in c.arg(0).children():
                locals()['$X' + num] = Int('$X' + num)
                new_var().append(locals()['$X' + num])
                num += 1
                tmp_children.append(locals()['$X' + num]==arg)

            tmp_children.append(func_op(func(*[new_var]), c.arg(1)))
            children.append(And(tmp_children))

    if op == 'and':
        return And(children)
    elif op == 'or':
        return Or(children)
    else:
        return Not(children)



def has_func(clause):
    children = clause.children()

# TODO: 删除不合法子句，少用check_sat
def check_legal(clause):
    pass