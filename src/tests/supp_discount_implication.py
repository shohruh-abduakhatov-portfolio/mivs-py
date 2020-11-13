from __future__ import print_function

import numpy as np
from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = 50

sum1 = model.NewIntVar(0, 1, "sum1")
sum2 = model.NewIntVar(0, 1, "sum2")
sum3 = model.NewIntVar(0, 1, "sum3")

a1 = model.NewIntVar(0, 10, "a1")
a2 = model.NewIntVar(0, 10, "a2")
a3 = model.NewIntVar(0, 10, "a3")

b1 = model.NewIntVar(0, 1, "b1")
b2 = model.NewIntVar(0, 1, "b2")
b3 = model.NewIntVar(0, 1, "b3")


model.Add(sum1 == 0).OnlyEnforceIf(b1)
model.Add(sum1 != 0).OnlyEnforceIf(b1.Not())
model.Add(sum2 == 0).OnlyEnforceIf(b2)
model.Add(sum2 != 0).OnlyEnforceIf(b2.Not())
model.Add(sum3 == 0).OnlyEnforceIf(b3)
model.Add(sum3 != 0).OnlyEnforceIf(b3.Not())

model.Add(a1 == a1 + 20).OnlyEnforceIf(b1)
model.Add(a1 == a1     ).OnlyEnforceIf(b1.Not())
model.Add(a2 == a2 + 20).OnlyEnforceIf(b2)
model.Add(a2 == a2     ).OnlyEnforceIf(b2.Not())
model.Add(a3 == a3 + 20).OnlyEnforceIf(b3)
model.Add(a3 == a3     ).OnlyEnforceIf(b3.Not())

# model.Add(a1 >= a1*sum1)
# model.Add(a2 >= a2*sum2)
# model.Add(a3 >= a3*sum3)

total = a1+a2+a3

# model.Minimize(1000-total)
model.Add(total <= 1000)
model.Maximize(total)


print("Solving")
solver = cp_model.CpSolver()
# solver.parameters.num_search_workers = 2
solver.parameters.max_time_in_seconds = 60.
status = solver.Solve(model)

# Print Solution
print()
print('  - status          : %s' % solver.StatusName(status), '(code:', status, ')')
print('  - conflicts       : %i' % solver.NumConflicts())
print('  - branches        : %i' % solver.NumBranches())
print('  - wall time       : %f ms' % solver.WallTime())
print()
print("@@@@@@@@@@@@@@@@@@@@@@@")
if status == 2 or status == 4:
    print('a1 = ', str(solver.Value(a1)), ' b1 = ', str(solver.Value(b1)))#, ' b1 = ', str(solver.BooleanValue(b1)))
    print('a2 = ', str(solver.Value(a2)), ' b2 = ', str(solver.Value(b2)))#, ' b2 = ', str(solver.BooleanValue(b2)))
    print('a3 = ', str(solver.Value(a3)), ' b3 = ', str(solver.Value(b3)))#, ' b3 = ', str(solver.BooleanValue(b3)))
