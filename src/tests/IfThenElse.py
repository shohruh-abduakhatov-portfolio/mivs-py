"""Solves a problem with a time limit."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


def SolveWithTimeLimitSampleSat():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()
    # Creates the variables.
    num_vals = 10
    cost = model.NewIntVar(0, 10, "cost")

    per11 = model.NewIntVar(0, 10, 'per11')
    per12 = model.NewIntVar(0, 10, 'per12')
    per13 = model.NewIntVar(0, 10, 'per13')

    per11_b = model.NewBoolVar('per11_b')
    per12_b = model.NewBoolVar('per12_b')
    per13_b = model.NewBoolVar('per13_b')
    print(per13_b)

    # UNCOMMENT To Add an all-different constraint.
    # model.AddBoolAnd([per12_b.Not(), per13_b.Not()]).OnlyEnforceIf(per11_b)
    # model.AddBoolAnd([per12_b.Not(), per11_b.Not()]).OnlyEnforceIf(per13_b)
    # model.AddBoolAnd([per11_b.Not(), per13_b.Not()]).OnlyEnforceIf(per12_b)
    model.Add(per11 == 3).OnlyEnforceIf(per11_b)
    model.Add(per12 == 9).OnlyEnforceIf(per12_b)
    model.Add(per13 == 8).OnlyEnforceIf(per13_b)
    model.Add(per11 == 0).OnlyEnforceIf(per11_b.Not())
    model.Add(per12 == 0).OnlyEnforceIf(per12_b.Not())
    model.Add(per13 == 0).OnlyEnforceIf(per13_b.Not())

    """Total cost"""

    # model.Add(sum([per11, per12, per13]) >= cost)
    model.Add(sum([per11, per12, per13]) == cost)

    model.Maximize(cost)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print('per11 = %i' % solver.Value(per11))
        print('per12 = %i' % solver.Value(per12))
        print('per13 = %i' % solver.Value(per13))




if __name__ == "__main__":
    SolveWithTimeLimitSampleSat()