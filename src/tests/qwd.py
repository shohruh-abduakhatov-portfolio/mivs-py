import numpy as np
from ortools.sat.python import cp_model
import itertools


model = cp_model.CpModel()
b = model.BoolVar('b')
x = model.IntVar(0, 10, 'x')
y = model.IntVar(0, 10, 'y')

model.Add(x + 2 * y == 5).OnlyEnforceIf(b.Not())

solver = cp_model.CpSolver()
# solver.parameters.num_search_workers = 7
solver.parameters.max_time_in_seconds = 60.
status = solver.Solve(model)
# Print Solution
print()
print('  - status          : %s' % solver.StatusName(status))
print('  - conflicts       : %i' % solver.NumConflicts())
print('  - branches        : %i' % solver.NumBranches())
print('  - wall time       : %f ms' % solver.WallTime())
print()