from __future__ import print_function

import numpy as np
from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = 50

sum1 = model.NewIntVar(0, 10, "sum1")
sum2 = model.NewIntVar(0, 10, "sum2")
sum3 = model.NewIntVar(0, 10, "sum3")

_sum1 = model.NewIntVar(0, 10, "_sum1")
_sum2 = model.NewIntVar(0, 10, "_sum2")
_sum3 = model.NewIntVar(0, 10, "_sum3")

a1 = model.NewIntVar(0, 1, "a1")
a2 = model.NewIntVar(0, 1, "a2")
a3 = model.NewIntVar(0, 1, "a3")


model.Add(sum1 >= sum1 + a1)
model.Add(sum2 >= sum2 + a2*1)
model.Add(sum3 >= sum3 + a3*1)

# total = a1+a2+a3
total_sum = sum1 + sum2 + sum3

# model.Add(total_sum==30)
model.Minimize(30 - total_sum)
model.Maximize(total_sum)


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
    print('sum1 = ', solver.Value(sum1))
    print('sum2 = ', solver.Value(sum2))
    print('sum3 = ', solver.Value(sum3))
