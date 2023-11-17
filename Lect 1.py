# Importing libraries
from pyomo.environ import *
import pandas as pd

#%%

'''
feasible
Obj: Maximize z
z = 500x + 400y

ST constriants
30x + 10y >= 135
10x + 15y <= 150
20x + 10y <= 160
x>=0
y>=0
x and y are positive

'''

# Using Concrete modelling not Abstract Modelling
prasanna_model = ConcreteModel()

# Write this line in the very beginning-for access to dual solution for constraints
prasanna_model.dual = Suffix(direction=Suffix.IMPORT)

# Tell Pyomo what your decision variables are
prasanna_model.x = Var(within=NonNegativeReals) # within=NonNegativeReals, initialize = 1.0
prasanna_model.y = Var(domain=PositiveReals)

# Tell pyomo what your constraints are
prasanna_model.Constraint1 = Constraint(expr = 30*prasanna_model.x + 10*prasanna_model.y >= 135)
prasanna_model.Constraint2 = Constraint(expr = 10*prasanna_model.x + 15*prasanna_model.y <= 150)
prasanna_model.Constraint3 = Constraint(expr = 20*prasanna_model.x + 10*prasanna_model.y <= 160)

# Tell pyomo what yout objective function is
prasanna_model.prasanna_goal = Objective(expr = 500*prasanna_model.x + 400*prasanna_model.y, sense=maximize)

# Tell pyomo to solve for x and y (decision variables)
optimizer = SolverFactory("glpk") # Using 'ipopt', 'glpk', 'gurobi', 'cplex', 'scip'
result = optimizer.solve(prasanna_model)
prasanna_model.display() # display overall model with values

# Print solver status
print(result.solver.status) # ok, warning
print(result.solver.termination_condition) # optimal, infeasible, unbounded, other

# Grab decision variables and objective value to us them somewhere else
print(prasanna_model.x.value) # prasanna_model.x(), value(prasanna_model.x)
print(prasanna_model.y.value)
print(value(prasanna_model.prasanna_goal)) # prasanna_model.prasanna_goal()
# Print all decision variable names defined in prasanna_model
for i in prasanna_model.component_objects(Var, descend_into=True):
    print(f"{i}")
    print(f"{i.name}")
    print(f"{value(i)}")

# Grab constraint's used up value
prasanna_model.Constraint1()
# Print constraint expressions and bounds defined in prasanna_model
prasanna_model.Constraint1.pprint() # print your constraint (expression) and bounds for easy reading and documenting
print(prasanna_model.Constraint1.body) # print your constraint body (expression)
print(prasanna_model.Constraint1.upper) # print your constraints ub
print(prasanna_model.Constraint1.lower) # print your constraints lb
# Print all constraint names and used up value defined in prasanna_model
for i in prasanna_model.component_objects(Constraint, descend_into=True):
    print(f"{i}")
    print(f"{i.name}")
    print(f"{value(i)}")
    print(f"{i.expr}")

# Sensitivity analysis / Postoptimality analysis
prasanna_model.Constraint1.slack() # left over RHS
prasanna_model.Constraint1.uslack() # Allowing increase in RHS
prasanna_model.Constraint1.lslack() # Allowing decrease in RHS
prasanna_model.dual[prasanna_model.Constraint1] # Shadow price / Dual price

#%%

'''
infeasible
Obj: Maximize z
z = 4x1 + 3x2

ST constriants
2x1 - x2 >= 6
x1 + x2 <= 2
x1 and x2 >= 0

'''

# Using Concrete modelling not Abstract Modelling
sabbella_model = ConcreteModel()

# Tell Pyomo what your decision variables are
sabbella_model.x1 = Var(within=NonNegativeReals, initialize=0.0)
sabbella_model.x2 = Var(within=NonNegativeReals, initialize=0.0)

# Tell pyomo what your constraints are
sabbella_model.Constraint1 = Constraint(expr = 2*sabbella_model.x1 - sabbella_model.x2 >= 6)
sabbella_model.Constraint2 = Constraint(expr = sabbella_model.x1 + sabbella_model.x2 <= 2)

# Tell pyomo what yout objective function is
sabbella_model.object = Objective(expr = 4*sabbella_model.x1 + 3*sabbella_model.x2, sense=maximize)

# Tell pyomo to solve for x and y (decision variables)
optimizer = SolverFactory("scip")
result = optimizer.solve(sabbella_model)
sabbella_model.display()

#%%

'''
unbounded
Obj: Maximize z
z = 2x1 + 3x2

ST constriants
x1 + x2 >= 3
x1 - 2x2 <= 4
x1 and x2 >= 0

'''
# Using Concrete modelling not Abstract Modelling
kumar_model = ConcreteModel()

# Tell Pyomo what your decision variables are
kumar_model.x1 = Var(within=NonNegativeReals, initialize = 0)
kumar_model.x2 = Var(within=NonNegativeReals, initialize = 0)

# Tell pyomo what your constraints are
kumar_model.Constraint1 = Constraint(expr = 1*kumar_model.x1 + 1*kumar_model.x2 >= 3)
kumar_model.Constraint2 = Constraint(expr = 1*kumar_model.x1 - 2*kumar_model.x2 <= 4)

# Tell pyomo what yout objective function is
kumar_model.object = Objective(expr = 2*kumar_model.x1 + 3*kumar_model.x2, sense=maximize) # minimize

# Tell pyomo to solve for x and y (decision variables)
optimizer = SolverFactory("scip") # Using 'ipopt', 'scip', 'gurobi', 'cplex'
result = optimizer.solve(kumar_model)
kumar_model.display()
#%%
'''
Pallet making problem
Obj: Maximize z
z = 10s + 9p

ST constriants
0.7s + p <= 630
6s + 4p <= 4320
0.1s + 0.2p <= 135
s and p >= 0

'''
# Using Concrete modelling not Abstract Modelling
pallet_model = ConcreteModel()

# Tell Pyomo what your decision variables are
pallet_model.s = Var(within=NonNegativeReals) # PositiveIntegers
pallet_model.p = Var(within=NonNegativeReals) # PositiveIntegers

# Tell pyomo what your constraints are
pallet_model.woodconstraint = Constraint(expr = 0.7*pallet_model.s + pallet_model.p <= 630)
pallet_model.timeconstraint = Constraint(expr = 6*pallet_model.s + 4*pallet_model.p <= 4320)
pallet_model.paintconstraint = Constraint(expr = 0.1*pallet_model.s + 0.2*pallet_model.p <= 135)

# Tell pyomo what yout objective function is
pallet_model.object = Objective(expr = 10*pallet_model.s + 9*pallet_model.p, sense=maximize)

# Tell pyomo to solve for x and y (decision variables)
optimizer = SolverFactory("scip")
result = optimizer.solve(pallet_model)
pallet_model.display()

#%%
'''
Pallet making or relocating
Obj: Maximize z
z = 2.5(h_std) + 1.75(h_prem) + 2.9(h_uprem) + 
    2.8(r_std) + 2.5(r_prem) + 3.25(r_uprem)

ST constriants
0.05(h_std) + 0.04(h_prem) + 0.01(h_uprem) <= 24
h_std + r_std = 2000
h_prem + r_prem = 3500
h_uprem + r_uprem = 1800
All 6 variables are +ve 

'''
# Using Concrete modelling not Abstract Modelling
pallet_model = ConcreteModel()

# Tell Pyomo what your decision variables are
pallet_model.h_std = Var(within=NonNegativeReals)
pallet_model.h_prem = Var(within=NonNegativeReals)
pallet_model.h_uprem = Var(within=NonNegativeReals)
pallet_model.r_std = Var(within=NonNegativeReals)
pallet_model.r_prem = Var(within=NonNegativeReals)
pallet_model.r_uprem = Var(within=NonNegativeReals)

# Tell pyomo what your constraints are
pallet_model.timeconstraint1 = Constraint(expr = 0.05*pallet_model.h_std + 0.04*pallet_model.h_prem + 0.01*pallet_model.h_uprem <= 24)
pallet_model.mandatorydemand1 = Constraint(expr = pallet_model.h_std + pallet_model.r_std >= 2000)
pallet_model.mandatorydemand2 = Constraint(expr = pallet_model.h_prem + pallet_model.r_prem >= 3500)
pallet_model.mandatorydemand3 = Constraint(expr = pallet_model.h_uprem + pallet_model.r_uprem >= 1800)

# Tell pyomo what yout objective function is
pallet_model.object = Objective(expr = 2.5*pallet_model.h_std + 1.75*pallet_model.h_prem + 2.9*pallet_model.h_uprem + 
    2.8*pallet_model.r_std + 2.5*pallet_model.r_prem + 3.25*pallet_model.r_uprem, sense=minimize)

# Tell pyomo to solve for x and y (decision variables)
optimizer = SolverFactory("scip")
result = optimizer.solve(pallet_model)
pallet_model.display()

#%%
# Transportation problem
'''
Daily Outbound Capacity By Truckload
x_UTK8_SAMS + x_UTK8_TRGT + x_UTK8_WLMT + x_UTK8_COST <= 40
x_USYP_SAMS + x_USYP_TRGT + x_USYP_WLMT + x_USYP_COST <= 108
x_UTAB_SAMS + x_UTAB_TRGT + x_UTAB_WLMT + x_UTAB_COST <= 61

Demands at DGLIDS
x_UTK8_SAMS + x_USYP_SAMS + x_UTAB_SAMS <= 42
x_UTK8_TRGT + x_USYP_TRGT + x_UTAB_TRGT <= 91
x_UTK8_WLMT + x_USYP_WLMT + x_UTAB_WLMT <= 20
x_UTK8_COST + x_USYP_COST + x_UTAB_COST <= 56

Minimize total cost
120*x_UTK8_SAMS + 130*x_UTK8_TRGT + ... + 14*x_UTK8_TRGT

'''
df = pd.read_excel('C:\\Users\\sabbe\\Desktop\\Ravali OR\\Transportation_problem.xlsx',sheet_name = "Sheet1")

# Using Concrete modelling not Abstract Modelling
transportation_model = ConcreteModel()

# Tell Pyomo what your decision variables are
transportation_model.x_UTK8_SAMS = Var(within=NonNegativeReals)
transportation_model.x_UTK8_TRGT = Var(within=NonNegativeReals)
transportation_model.x_UTK8_WLMT = Var(within=NonNegativeReals)
transportation_model.x_UTK8_COST = Var(within=NonNegativeReals)
transportation_model.x_USYP_SAMS = Var(within=NonNegativeReals)
transportation_model.x_USYP_TRGT = Var(within=NonNegativeReals)
transportation_model.x_USYP_WLMT = Var(within=NonNegativeReals)
transportation_model.x_USYP_COST = Var(within=NonNegativeReals)
transportation_model.x_UTAB_SAMS = Var(within=NonNegativeReals)
transportation_model.x_UTAB_TRGT = Var(within=NonNegativeReals)
transportation_model.x_UTAB_WLMT = Var(within=NonNegativeReals)
transportation_model.x_UTAB_COST = Var(within=NonNegativeReals)

# Defining constants in Python not pyomo
c_UTK8_SAMS = df.loc[df['SC'] == 'UTK8', 'SAMS'].item()
c_UTK8_TRGT = df.loc[df['SC'] == 'UTK8', 'TARGET'].item()
c_UTK8_WLMT = df.loc[df['SC'] == 'UTK8', 'WALMART'].item()
c_UTK8_COST = df.loc[df['SC'] == 'UTK8', 'COSTCO'].item()
c_USYP_SAMS = df.loc[df['SC'] == 'USYP', 'SAMS'].item()
c_USYP_TRGT = df.loc[df['SC'] == 'USYP', 'TARGET'].item()
c_USYP_WLMT = df.loc[df['SC'] == 'USYP', 'WALMART'].item()
c_USYP_COST = df.loc[df['SC'] == 'USYP', 'COSTCO'].item()
c_UTAB_SAMS = df.loc[df['SC'] == 'UTAB', 'SAMS'].item()
c_UTAB_TRGT = df.loc[df['SC'] == 'UTAB', 'TARGET'].item()
c_UTAB_WLMT = df.loc[df['SC'] == 'UTAB', 'WALMART'].item()
c_UTAB_COST = df.loc[df['SC'] == 'UTAB', 'COSTCO'].item()

# Tell pyomo what your constraints are
transportation_model.UTK8_DOC = Constraint(expr = transportation_model.x_UTK8_SAMS+transportation_model.x_UTK8_TRGT+transportation_model.x_UTK8_WLMT+transportation_model.x_UTK8_COST <= 40)
transportation_model.USYP_DOC = Constraint(expr = transportation_model.x_USYP_SAMS+transportation_model.x_USYP_TRGT+transportation_model.x_USYP_WLMT+transportation_model.x_USYP_COST <= 108)
transportation_model.UTAB_DOC = Constraint(expr = transportation_model.x_UTAB_SAMS+transportation_model.x_UTAB_TRGT+transportation_model.x_UTAB_WLMT+transportation_model.x_UTAB_COST <= 61)
transportation_model.SAMS_DMD = Constraint(expr = transportation_model.x_UTK8_SAMS+transportation_model.x_USYP_SAMS+transportation_model.x_UTAB_SAMS == 42)
transportation_model.TRGT_DMD = Constraint(expr = transportation_model.x_UTK8_TRGT+transportation_model.x_USYP_TRGT+transportation_model.x_UTAB_TRGT == 91)
transportation_model.WLMT_DMD = Constraint(expr = transportation_model.x_UTK8_WLMT+transportation_model.x_USYP_WLMT+transportation_model.x_UTAB_WLMT == 20)
transportation_model.COST_DMD = Constraint(expr = transportation_model.x_UTK8_COST+transportation_model.x_USYP_COST+transportation_model.x_UTAB_COST == 56)


# Tell pyomo what your objective function is
transportation_model.ravali = Objective(expr = c_UTK8_SAMS*transportation_model.x_UTK8_SAMS+
                                        c_UTK8_TRGT*transportation_model.x_UTK8_TRGT+
                                        c_UTK8_WLMT*transportation_model.x_UTK8_WLMT+
                                        c_UTK8_COST*transportation_model.x_UTK8_COST+
                                        c_USYP_SAMS*transportation_model.x_USYP_SAMS+
                                        c_USYP_TRGT*transportation_model.x_USYP_TRGT+
                                        c_USYP_WLMT*transportation_model.x_USYP_WLMT+
                                        c_USYP_COST*transportation_model.x_USYP_COST+
                                        c_UTAB_SAMS*transportation_model.x_UTAB_SAMS+
                                        c_UTAB_TRGT*transportation_model.x_UTAB_TRGT+
                                        c_UTAB_WLMT*transportation_model.x_UTAB_WLMT+
                                        c_UTAB_COST*transportation_model.x_UTAB_COST , sense=minimize)


# Tell pyomo to solve for decision variables
optimizer = SolverFactory("scip")
result = optimizer.solve(transportation_model)
transportation_model.display()
#%%
###
#%%