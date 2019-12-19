from z3 import *

def DNF2program(clause, func):
    def_domain = []
    val_domain = 0


class program():
    def __init__(self, clause):
        self.clause = clause
        self.def_domain = []
        self.val_domain = 0
        self.vars = []

    def var_sub(self):
        for c in self.clause.children():
            if c.decl().name() == '==':
                self.vars = c.arg(0).children()
                self.val_domain = c.arg(1)
        children = []
        for c in self.clause.children():
            if c.decl().name() == '==':
                children.append(c)
            elif c.arg(0).children() == self.vars:
                op = c.arg(0).decl()
                children.append(And(op(self.val_domain, c.arg(1))))



def solver(clause):
    pass