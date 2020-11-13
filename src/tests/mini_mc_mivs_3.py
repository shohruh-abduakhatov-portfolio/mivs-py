"""Solves a problem with a time limit."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


def SolveWithTimeLimitSampleSat():
    model = cp_model.CpModel()
    product = ["Product_1", "Product_2"]

    drug_qnty_req = [10, 15]
    input_capital = 15009000
    cash = 150000
    perech = 15009000 - 150000
    supplier = ["S1",
                "S2",
                "S3",
                "S4"]
    cash_cost = [[400, 200, 150, 500], [400, 200, 150, 500]]
    pred_100 = [[440, 220, 165, 550], [400, 200, 150, 500]]
    pred_50 = [[400, 204, 153, 510], [400, 200, 150, 500]]
    pred_25 = [[420, 210, 158, 6], [5, 200, 150, 500]]

    per1_ = model.NewIntVar(0, drug_qnty_req[0], 'per11')
    per12 = model.NewIntVar(0, drug_qnty_req[0], 'per12')
    per13 = model.NewIntVar(0, drug_qnty_req[0], 'per13')
    per14 = model.NewIntVar(0, drug_qnty_req[0], 'per14')
    per2_ = model.NewIntVar(0, drug_qnty_req[1], 'per21')
    per22 = model.NewIntVar(0, drug_qnty_req[1], 'per22')
    per23 = model.NewIntVar(0, drug_qnty_req[1], 'per23')
    per24 = model.NewIntVar(0, drug_qnty_req[1], 'per24')

    per3_ = model.NewIntVar(0, drug_qnty_req[2], 'per31')
    per32 = model.NewIntVar(0, drug_qnty_req[2], 'per32')
    per33 = model.NewIntVar(0, drug_qnty_req[2], 'per33')
    per34 = model.NewIntVar(0, drug_qnty_req[2], 'per34')
    per4_ = model.NewIntVar(0, drug_qnty_req[3], 'per41')
    per42 = model.NewIntVar(0, drug_qnty_req[3], 'per42')
    per43 = model.NewIntVar(0, drug_qnty_req[3], 'per43')
    per44 = model.NewIntVar(0, drug_qnty_req[3], 'per44')

    per1_bool = model.NewBoolVar('per11_bool')
    per12_bool = model.NewBoolVar('per12_bool')
    per13_bool = model.NewBoolVar('per13_bool')
    per14_bool = model.NewBoolVar('per14_bool')
    per2_bool = model.NewBoolVar('per21_bool')
    per22_bool = model.NewBoolVar('per22_bool')
    per23_bool = model.NewBoolVar('per23_bool')
    per24_bool = model.NewBoolVar('per24_bool')

    per3_bool = model.NewBoolVar('per31_bool')
    per32_bool = model.NewBoolVar('per32_bool')
    per33_bool = model.NewBoolVar('per33_bool')
    per34_bool = model.NewBoolVar('per34_bool')
    per4_bool = model.NewBoolVar('per41_bool')
    per42_bool = model.NewBoolVar('per42_bool')
    per43_bool = model.NewBoolVar('per43_bool')
    per44_bool = model.NewBoolVar('per44_bool')

    # Adds an all-different constraint.
    # model.AddBoolAnd([per12_bool.Not(), per13_bool.Not(), per14_bool.Not()]).OnlyEnforceIf(per1_bool)

    model.Add(per1_ == drug_qnty_req[0]).OnlyEnforceIf(per1_bool)
    model.Add(per1_ == 0).OnlyEnforceIf(per1_bool.Not())
    model.Add(per12 == drug_qnty_req[0]).OnlyEnforceIf(per12_bool)
    model.Add(per12 == 0).OnlyEnforceIf(per12_bool.Not())
    model.Add(per13 == drug_qnty_req[0]).OnlyEnforceIf(per13_bool)
    model.Add(per13 == 0).OnlyEnforceIf(per13_bool.Not())
    model.Add(per14 == drug_qnty_req[0]).OnlyEnforceIf(per14_bool)
    model.Add(per14 == 0).OnlyEnforceIf(per14_bool.Not())
    model.Add(per2_ == 10).OnlyEnforceIf(per2_bool)
    model.Add(per2_ == 0).OnlyEnforceIf(per2_bool.Not())
    model.Add(per22 == drug_qnty_req[1]).OnlyEnforceIf(per22_bool)
    model.Add(per22 == 0).OnlyEnforceIf(per22_bool.Not())
    model.Add(per23 == drug_qnty_req[1]).OnlyEnforceIf(per23_bool)
    model.Add(per23 == 0).OnlyEnforceIf(per23_bool.Not())
    model.Add(per24 == drug_qnty_req[1]).OnlyEnforceIf(per24_bool)
    model.Add(per24 == 0).OnlyEnforceIf(per24_bool.Not())

    model.Add(per3_ == drug_qnty_req[2]).OnlyEnforceIf(per3_bool)
    model.Add(per3_ == 0).OnlyEnforceIf(per3_bool.Not())
    model.Add(per32 == drug_qnty_req[2]).OnlyEnforceIf(per32_bool)
    model.Add(per32 == 0).OnlyEnforceIf(per32_bool.Not())
    model.Add(per33 == drug_qnty_req[2]).OnlyEnforceIf(per33_bool)
    model.Add(per33 == 0).OnlyEnforceIf(per33_bool.Not())
    model.Add(per34 == drug_qnty_req[2]).OnlyEnforceIf(per34_bool)
    model.Add(per34 == 0).OnlyEnforceIf(per34_bool.Not())
    model.Add(per4_ == 10).OnlyEnforceIf(per4_bool)
    model.Add(per4_ == 0).OnlyEnforceIf(per4_bool.Not())
    model.Add(per42 == drug_qnty_req[3]).OnlyEnforceIf(per42_bool)
    model.Add(per42 == 0).OnlyEnforceIf(per42_bool.Not())
    model.Add(per43 == drug_qnty_req[3]).OnlyEnforceIf(per43_bool)
    model.Add(per43 == 0).OnlyEnforceIf(per43_bool.Not())
    model.Add(per44 == drug_qnty_req[3]).OnlyEnforceIf(per44_bool)
    model.Add(per44 == 0).OnlyEnforceIf(per44_bool.Not())

    model.AddBoolAnd([per12_bool.Not(), per13_bool.Not(), per14_bool.Not(), per2_bool, per1_bool]).OnlyEnforceIf(per1_bool)
    model.AddBoolAnd([per1_bool.Not(), per13_bool.Not(), per14_bool.Not(), per22_bool, per12_bool]).OnlyEnforceIf(per12_bool)
    model.AddBoolAnd([per1_bool.Not(), per12_bool.Not(), per14_bool.Not(), per23_bool, per13_bool]).OnlyEnforceIf(per13_bool)
    model.AddBoolAnd([per1_bool.Not(), per12_bool.Not(), per13_bool.Not(), per24_bool, per14_bool]).OnlyEnforceIf(per14_bool)
    model.AddBoolAnd([per22_bool.Not(), per23_bool.Not(), per24_bool.Not(), per1_bool, per2_bool]).OnlyEnforceIf(per2_bool)
    model.AddBoolAnd([per2_bool.Not(), per23_bool.Not(), per24_bool.Not(), per12_bool, per22_bool]).OnlyEnforceIf(per22_bool)
    model.AddBoolAnd([per2_bool.Not(), per22_bool.Not(), per24_bool.Not(), per13_bool, per23_bool]).OnlyEnforceIf(per23_bool)
    model.AddBoolAnd([per2_bool.Not(), per22_bool.Not(), per23_bool.Not(), per14_bool, per24_bool]).OnlyEnforceIf(per24_bool)

    model.AddBoolAnd([per32_bool.Not(), per33_bool.Not(), per34_bool.Not(), per4_bool, per3_bool]).OnlyEnforceIf(per3_bool)
    model.AddBoolAnd([per3_bool.Not(), per33_bool.Not(), per34_bool.Not(), per42_bool, per32_bool]).OnlyEnforceIf(per32_bool)
    model.AddBoolAnd([per3_bool.Not(), per32_bool.Not(), per34_bool.Not(), per43_bool, per33_bool]).OnlyEnforceIf(per33_bool)
    model.AddBoolAnd([per3_bool.Not(), per32_bool.Not(), per33_bool.Not(), per44_bool, per34_bool]).OnlyEnforceIf(per34_bool)
    model.AddBoolAnd([per42_bool.Not(), per43_bool.Not(), per44_bool.Not(), per3_bool, per4_bool]).OnlyEnforceIf(per4_bool)
    model.AddBoolAnd([per4_bool.Not(), per43_bool.Not(), per44_bool.Not(), per32_bool, per42_bool]).OnlyEnforceIf(per42_bool)
    model.AddBoolAnd([per4_bool.Not(), per42_bool.Not(), per44_bool.Not(), per33_bool, per43_bool]).OnlyEnforceIf(per43_bool)
    model.AddBoolAnd([per4_bool.Not(), per42_bool.Not(), per43_bool.Not(), per34_bool, per44_bool]).OnlyEnforceIf(per44_bool)

    # model.AddMaxEquality()

    """Total cost"""
    qnty_diff1 = sum([per1_, per12, per13, per14]) - drug_qnty_req[0]
    qnty_diff2 = sum([per2_, per22, per23, per24]) - drug_qnty_req[1]
    qnty_diff3 = sum([per3_, per32, per33, per34]) - drug_qnty_req[2]
    qnty_diff4 = sum([per4_, per42, per43, per44]) - drug_qnty_req[3]
    total_sum = sum([per1_ * prices1[0], per12 * prices1[1], per13 * prices1[2], per14 * prices1[3],
                     per2_ * prices2[0], per22 * prices2[1], per23 * prices2[2], per24 * prices2[3],
                     per3_ * prices3[0], per32 * prices3[1], per33 * prices3[2], per34 * prices3[3],
                     per4_ * prices4[0], per42 * prices4[1], per43 * prices4[2], per44 * prices4[3]
                     ])

    model.Add((per1_ * prices1[0] + per2_ * prices2[0] + per3_ * prices3[0] + per4_ * prices4[0]) <= cash)
    model.Add(sum([per12 * prices1[1], per13 * prices1[2], per14 * prices1[3],
                   per22 * prices2[1], per23 * prices2[2], per24 * prices2[3],
                   per42 * prices4[1], per43 * prices4[2], per44 * prices4[3],
                   per32 * prices3[1], per33 * prices3[2], per34 * prices3[3]
                   ]) <= perech)
    model.Add(total_sum <= input_capital)
    model.Add(qnty_diff1 >= 0)
    model.Add(qnty_diff2 >= 0)
    model.Add(qnty_diff3 >= 0)
    model.Add(qnty_diff4 >= 0)

    # model.Minimize(qnty_diff)
    model.Maximize(input_capital - total_sum)
    model.Minimize(total_sum)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    # solver.parameters.max_time_in_seconds = 10.0
    # solver.parameters.num_search_workers = 7
    solver.parameters.max_time_in_seconds = 60.
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        print('per1_ = %i, per2_ = %i' % (solver.Value(per1_), solver.Value(per2_)))
        print('per12 = %i, per22 = %i' % (solver.Value(per12), solver.Value(per22)))
        print('per13 = %i, per23 = %i' % (solver.Value(per13), solver.Value(per23)))
        print('per14 = %i, per24 = %i' % (solver.Value(per14), solver.Value(per24)))
        print()
        print('per3_ = %i, per4_ = %i' % (solver.Value(per3_), solver.Value(per4_)))
        print('per32 = %i, per42 = %i' % (solver.Value(per32), solver.Value(per42)))
        print('per33 = %i, per43 = %i' % (solver.Value(per33), solver.Value(per43)))
        print('per34 = %i, per44 = %i' % (solver.Value(per34), solver.Value(per44)))

    print()
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())


SolveWithTimeLimitSampleSat()
