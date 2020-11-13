
from ortools.sat.python import cp_model
# model = cp_model.CpModel()
import numpy as np
import itertools


def all_diff(model, num_prod, num_sup, num_perech, bools_list):
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # Adds an all-different constrai12. Select one price per row of all perechs.
            # If one perech price is selected -> do not select other perech price variants
            for k in range(num_perech + 1):
                i_same_sup_bools = []
                for i_in in np.arange(num_prod):
                    i_same_sup_bools.append(bools_list[i_in][j][:k] + bools_list[i_in][j][k + 1:])

                i_same_sup_bools = list(itertools.chain(*i_same_sup_bools))
                for i_in in range(len(i_same_sup_bools)):
                    i_same_sup_bools[i_in] = i_same_sup_bools[i_in].Not()
                model.AddBoolAnd(i_same_sup_bools).OnlyEnforceIf(bools_list[i][j][k])
    return model

