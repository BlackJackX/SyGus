from z3 import *
from hjk.translator import *


class MyChecker:
    def __init__(self, program, checker):
        self.checker = checker
        self.pts = []
        self.program = program
        self.pts.append(self.create_counterexample())

    def create_counterexample(self):
        spec_smt2 = [' '.join(['(', 'declare-fun', self.checker.synFunction.name,\
                               '(', ' '.join(list(map(lambda l: str(l[1]),
                                                      self.checker.synFunction.argList))), ')',
                               self.checker.synFunction.retSort, ')'])]
        for constraint in self.checker.Constraints:
            spec_smt2.append('(assert %s)' % (toString(constraint[1:])))
        spec_smt2 = '\n'.join(spec_smt2)
        spec = parse_smt2_string(spec_smt2, decls=dict(self.checker.VarTable))
        spec = And(spec)
        self.solver = Solver()
        self.solver.add(spec)
        self.solver.check()
        model = self.solver.model()
        self.solver.push()
        return model

    def check(self):
        prog_smt = parse_smt2_string(self.program)
        self.solver.add(prog_smt)
        self.solver.push()

        for m in self.pts:
            ce = []
            for v in self.checker.VarTable.values():
                ce.append(v==m.get_interp(v))

            vars = list(map(lambda x: str(x), self.checker.VarTable))
            func = list(filter(lambda x: not str(x) in vars, m.decls()))

            if func != []:
                func = func[0]
                funcMap = m.get_interp(func).as_list()
                for item in funcMap:
                    if not isinstance(item, list):
                        continue
                    ce.append(self.checker.synFunction.targetFunction(int(item[0]))==item[1])
                self.solver.add(And(ce))
            self.solver.push()
            if self.solver.check() == 'unsat':
                self.solver.pop()
                self.solver.pop()
                return (True, None)

            self.solver.pop()
        self.solver.pop()
        counterexample = self.checker.check(self.program)
        return (False, counterexample)

