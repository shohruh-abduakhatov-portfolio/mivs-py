"""Solves a problem with a time limit."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


def SolveWithTimeLimitSampleSat():
    model = cp_model.CpModel()
    req_qnty = [10, 10]
    input_capital = 100000
    cash = int(input_capital * 0.5)
    perech = input_capital - cash
    # prices = [10, 0, 0, 0]
    # prices = [0, 10, 0, 0]
    prices1 = [10, 11, 1221, 12]
    prices2 = [9, 1221, 1221, 10]

    per1_ = model.NewIntVar(0, req_qnty[0] ** 2, 'per11')
    per12 = model.NewIntVar(0, req_qnty[0] ** 2, 'per12')
    per13 = model.NewIntVar(0, req_qnty[0] ** 2, 'per13')
    per14 = model.NewIntVar(0, req_qnty[0] ** 2, 'per14')

    per2_ = model.NewIntVar(0, req_qnty[1] ** 2, 'per21')
    per22 = model.NewIntVar(0, req_qnty[1] ** 2, 'per22')
    per23 = model.NewIntVar(0, req_qnty[1] ** 2, 'per23')
    per24 = model.NewIntVar(0, req_qnty[1] ** 2, 'per24')

    per1_bool = model.NewBoolVar('per11_bool')
    per12_bool = model.NewBoolVar('per12_bool')
    per13_bool = model.NewBoolVar('per13_bool')
    per14_bool = model.NewBoolVar('per14_bool')

    per2_bool = model.NewBoolVar('per21_bool')
    per22_bool = model.NewBoolVar('per22_bool')
    per23_bool = model.NewBoolVar('per23_bool')
    per24_bool = model.NewBoolVar('per24_bool')

    # Adds an all-different constraint.
    # model.AddBoolAnd([per12_bool.Not(), per13_bool.Not(), per14_bool.Not()]).OnlyEnforceIf(per1_bool)

    model.Add(per1_ <= 10).OnlyEnforceIf(per1_bool)
    model.Add(per1_ == 0).OnlyEnforceIf(per1_bool.Not())

    model.Add(per12 <= req_qnty[0] ** 2).OnlyEnforceIf(per12_bool)
    model.Add(per12 == 0).OnlyEnforceIf(per12_bool.Not())
    model.Add(per13 <= req_qnty[0] ** 2).OnlyEnforceIf(per13_bool)
    model.Add(per13 == 0).OnlyEnforceIf(per13_bool.Not())
    model.Add(per14 <= req_qnty[0] ** 2).OnlyEnforceIf(per14_bool)
    model.Add(per14 == 0).OnlyEnforceIf(per14_bool.Not())

    model.Add(per2_ <= 10).OnlyEnforceIf(per2_bool)
    model.Add(per2_ == 0).OnlyEnforceIf(per2_bool.Not())
    model.Add(per22 <= req_qnty[1] ** 2).OnlyEnforceIf(per22_bool)
    model.Add(per22 == 0).OnlyEnforceIf(per22_bool.Not())
    model.Add(per23 <= req_qnty[1] ** 2).OnlyEnforceIf(per23_bool)
    model.Add(per23 == 0).OnlyEnforceIf(per23_bool.Not())
    model.Add(per24 <= req_qnty[1] ** 2).OnlyEnforceIf(per24_bool)
    model.Add(per24 == 0).OnlyEnforceIf(per24_bool.Not())



    model.AddBoolAnd([per13_bool.Not(), per14_bool.Not()]).OnlyEnforceIf(per12_bool)
    model.AddBoolAnd([per12_bool.Not(), per14_bool.Not()]).OnlyEnforceIf(per13_bool)
    model.AddBoolAnd([per12_bool.Not(), per13_bool.Not()]).OnlyEnforceIf(per14_bool)

    model.AddBoolAnd([per23_bool.Not(), per24_bool.Not()]).OnlyEnforceIf(per22_bool)
    model.AddBoolAnd([per22_bool.Not(), per24_bool.Not()]).OnlyEnforceIf(per23_bool)
    model.AddBoolAnd([per22_bool.Not(), per23_bool.Not()]).OnlyEnforceIf(per24_bool)

    # model.AddMaxEquality()

    """Total cost"""
    qnty_diff1 = sum([per1_, per12, per13, per14]) - req_qnty[0]
    qnty_diff2 = sum([per2_, per22, per23, per24]) - req_qnty[1]
    total_sum = sum([per1_ * prices1[0], per12 * prices1[1], per13 * prices1[2], per14 * prices1[3],
                     per2_ * prices2[0], per22 * prices2[1], per23 * prices2[2], per24 * prices2[3]])

    model.Add((per1_ * prices1[0] + per2_ * prices2[0]) <= cash)
    model.Add(sum([per12 * prices1[1], per13 * prices1[2], per14 * prices1[3],
                   per22 * prices2[1], per23 * prices2[2], per24 * prices2[3]]) <= perech)
    model.Add(total_sum <= input_capital)
    model.Add(qnty_diff1 >= 0)
    model.Add(qnty_diff2 >= 0)

    # model.Minimize(qnty_diff)
    model.Maximize(input_capital - total_sum)
    model.Minimize(total_sum)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print('per1_ = %i' % solver.Value(per1_))
        print('per12 = %i' % solver.Value(per12))
        print('per13 = %i' % solver.Value(per13))
        print('per14 = %i' % solver.Value(per14))
        print('per2_ = %i' % solver.Value(per2_))
        print('per22 = %i' % solver.Value(per22))
        print('per23 = %i' % solver.Value(per23))
        print('per24 = %i' % solver.Value(per24))
    print()
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())


SolveWithTimeLimitSampleSat()
