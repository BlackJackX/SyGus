# translator
## ReadQuery
### local variable
    SynFunExpr //语法列表，0为synth-fun，1为函数名，2为参数，3为返回值，4为展开式规则列表
    VarTable //变量字典，str->z3的变量对象Int or Bool
    Constraints //限制列表，每个元素的，0为constrain，1为限制
    FunDefMap //函数字典，lia规则中为空
### return
    checker : 
        找到一个符合constrain但不符合function的变量取值model，也就是找到一个