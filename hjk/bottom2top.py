from z3 import *
from itertools import product
from hjk.CEGIS import *
from operator import eq
import time

start = 0
end = 0
T = 60*3

def b2t_search(bmExpr, checker):
    start = time.time()
    funcDefine = ' '.join(['define-fun', checker.synFunction.name, '(', ' '.join(list(map(lambda l: '(' + ' '.join(l) + ')', checker.synFunction.argList))), ')', checker.synFunction.retSort])
    intSet = [[],[]]
    boolSet = [[],[]]
    i2iops = []
    b2bops = []
    i2bops = []
    b2iops = ['ite']
    exprs = [intSet, boolSet]
    ops = [i2iops, b2bops, i2bops, b2iops]

    progSize = 1

    for e in bmExpr[1][4][0][2][:-1]:
        if isinstance(e, tuple):
            intSet[1].append(e[1])
        elif isinstance(e, list):
            if e[0] in ['+', '-', '*', '/', 'mod']:
                i2iops.append(e[0])
            elif e[0] in ['<=', '>=', '<', '>', '=']:
                i2bops.append(e[0])
            elif e[0] in ['or', 'and']:
                b2bops.append(e[0])
        elif isinstance(e, str):
            intSet[1].append(e)

    for e in bmExpr[1][4][1][2]:
        if isinstance(e, tuple):
            intSet[1].append(e[1])
        elif isinstance(e, list):
            if e[0] in ['+', '-', '*', '/', 'mod']:
                i2iops.append(e[0])
            elif e[0] in ['<=', '>=', '<', '>', '=']:
                i2bops.append(e[0])
            elif e[0] in ['or', 'and']:
                b2bops.append(e[0])
        elif isinstance(e, str):
            intSet[1].append(e)

    while True:
        mc = MyChecker('', checker)
        c = 1
        for ie in intSet[progSize]:
            end = time.time()
            if end-start > T:
                print('Not found!!!')
                return
            program = expr2prog(funcDefine, ie)
            mc.program = program
            """
            (conflict, counterexample) = mc.check()
            print("%d %s" %(c, program))
            c += 1

            if not conflict:
                if counterexample == None:
                    print(program)
                    return
                else:
                    mc.pts.append(counterexample)
            """
            counterexample = checker.check(program)
            print("%d %s" %(c, program))
            c += 1

        progSize += 1
        enum_exprs(exprs, progSize, ops)
        end = time.time()
        if end - start > T:
            print('Not found!!!')
            print(end, start)
            return
        #print(len(intSet[progSize]))
        cut_branch(exprs, progSize)

    print('Not found!!!')


def enum_exprs(exprs, progsize, ops):
    i2iops = ops[0]
    b2bops = ops[1]
    i2bops = ops[2]
    b2iops = ops[3]
    intSet = exprs[0]
    boolSet = exprs[1]
    intSet.append([])
    boolSet.append([])
    if progsize <= 1:
        for ps1 in range(1, progsize-1):
            ps2 = progsize-1-ps1
            intSet[progsize].extend(list(product(i2iops, intSet[ps1], intSet[ps2])))

    for ps1 in range(1, progsize-1):
        for ps2 in range(1, progsize-ps1-1):
            ps3 = progsize-1-ps1-ps2
            intSet[progsize].extend(list(product(b2iops, boolSet[ps1], intSet[ps2], intSet[ps3])))

    for ps1 in range(1, progsize-1):
        ps2 = progsize-1-ps1
        boolSet[progsize].extend(list(product(i2bops, intSet[ps1], intSet[ps2])))
    """
    for ps1 in range(1, progsize-1):
        ps2 = progsize-1-ps1
        boolSet[progsize].extend(list(product(b2bops, boolSet[ps1], boolSet[ps2])))
    """

def expr2prog(funcDefine, expr):
    return '(' + funcDefine + ' ' + muti2str(expr) + ')'

def muti2str(t):
    if not isinstance(t, tuple) and not isinstance(t, list):
        return str(t)
    return '('+' '.join(list(map(lambda x: muti2str(x), t)))+')'

def cut_branch(exprs, progSize):
    intSet = exprs[0][progSize]
    boolSet = exprs[1][progSize]

    intSet = list(filter(intfilter, intSet))

    boolSet = list(filter(boolfilter, boolSet))
    exprs[0][progSize] = intSet
    exprs[1][progSize] = boolSet

def intfilter(ie):
    if not isinstance(ie, list):
        return True
    op = ie[0]
    if op == 'ite':
        if eq(ie[2], ie[3]):
            return False
    return True

def boolfilter(be):
    if isinstance(be[1], int) or isinstance(be[2], int):
        return False
    if eq(be[1], be[2]):
        return False
    return True
