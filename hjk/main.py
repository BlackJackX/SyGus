import random
import sys
import sexp
import pprint
import translator
from hjk.transform import *
from hjk.bottom2top import *
from hjk.CEGIS import *


def Extend(Stmts,Productions):
    ret = []
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            TryExtend = Extend(Stmts[i],Productions)
            if len(TryExtend) > 0 :
                for extended in TryExtend:
                    ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        elif Stmts[i] in Productions.keys():
            randomExtended = Productions[Stmts[i]]
            random.shuffle(randomExtended)
            for extended in randomExtended:
                ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
    return ret

def stripComments(bmFile):
    noComments = '('
    for line in bmFile:
        line = line.split(';', 1)[0]
        noComments += line
    return noComments + ')'

# todo: insert new constrain
def appendConstrain(checker, counterexample):
    constrain = ['constrain', [], []]
    ce = [checker.synFunction.name]
    constrain[1].append('=')
    for arg in checker.synFunction.argList:
        ce.append(counterexample.eval[arg])


def constraints2prog(constraints, func):
    s1 = '(' + func[0] + ' ' + func[1] + ' '
    s2 = '('
    for v in func[2]:
        s2 += '(' + v[0] + ' ' + v[1] + ')'
    s2 += ')'
    s3 = ' ' + func[3] + ' ' + constraints + ')'
    return s1 + s2 + s3



def main():
    benchmarkFile = open(sys.argv[1])
    bm = stripComments(benchmarkFile)
    bmExpr = sexp.sexp.parseString(bm, parseAll=True).asList()[0] #Parse string to python list
    #pprint.pprint(bmExpr)
    checker=translator.ReadQuery(bmExpr)
    #print (checker.check('(define-fun f ((x Int)) Int (mod (* x 3) 10)  )'))
    #raw_input()
    SynFunExpr = []
    StartSym = 'My-Start-Symbol' #virtual starting symbol
    for expr in bmExpr:
        if len(expr)==0:
            continue
        elif expr[0]=='synth-fun':
            SynFunExpr=expr
    FuncDefine = ['define-fun']+SynFunExpr[1:4] #copy function signature
    #print(FuncDefine)
    BfsQueue = [[StartSym]] #Top-down
    Productions = {StartSym:[]}
    Type = {StartSym:SynFunExpr[3]} # set starting symbol's return type

    for NonTerm in SynFunExpr[4]: #SynFunExpr[4] is the production rules
        NTName = NonTerm[0]
        NTType = NonTerm[1]
        if NTType == Type[StartSym]:
            Productions[StartSym].append(NTName)
        Type[NTName] = NTType
        #Productions[NTName] = NonTerm[2]
        Productions[NTName] = []
        for NT in NonTerm[2]:
            if type(NT) == tuple:
                Productions[NTName].append(str(NT[1])) # deal with ('Int',0). You can also utilize type information, but you will suffer from these tuples.
            else:
                Productions[NTName].append(NT)

    b2t_search(bmExpr, checker)

    constraints = pipline(checker.Constraints)
    program = constraints2prog(constraints, FuncDefine)
    counterexample = checker.check(program)
    if counterexample is None:
        print(program)

if __name__ == '__main__':
    main()
