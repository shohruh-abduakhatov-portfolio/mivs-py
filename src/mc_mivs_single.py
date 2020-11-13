"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function

from datetime import time

import numpy as np
from ortools.sat.python import cp_model
from time import time


### todo
# 1. Change to Per-Supplier-Single Payment Method
#
# (+) 2. Check Constraints
# (+)      -> Minimize Total Payment
# (+)      -> Maximize diff but not 25% Priority
#
# 3. Max Val is the same as **2 instead of maximizing put 0
#       IOW, remove this part
#
# (+) 4. Calc ex(e)cution time each step: timeit()

_format = "%s_%s_%s"
format_cash = _format + "_cash"
format_perech = _format + "_perech"
format_bool = _format + "_bool"


async def main(product,
               req_qnty,
               input_capital,
               cash,
               perech,
               supplier,
               cash_cost,
               pred_100,
               pred_50,
               pred_25,
               prices_title,
               pred_50_prepay_ratio,
               pred_25_prepay_ratio):
    model = cp_model.CpModel()
    all_perechislenies = [pred_100, pred_50, pred_25]
    all_perechislenies_prep_ratio = [pred_100, pred_50_prepay_ratio, pred_25_prepay_ratio]
    # lengths
    num_prod = len(product)
    num_sup = len(supplier)
    num_perech = len(all_perechislenies)  # 3 apprx
    # empty product-supplier-cash-[perechs] dict
    cash_list = np.full(shape=(num_prod, num_sup, 1, 1), fill_value=0).tolist()
    perech_list = np.full(shape=(num_prod, num_sup, num_perech, 1), fill_value=0).tolist()
    bools_list = np.full(shape=(num_prod, num_sup, num_perech, 1), fill_value=0).tolist()

    """Declaring Variables"""
    now = time()
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            cash_list[i][j] = model.NewIntVar(0, req_qnty[i] ** 2, format_cash % (i, j, 0))
            for k in range(num_perech):
                perech_list[i][j][k] = model.NewIntVar(0, req_qnty[i] ** 2, format_perech % (i, j, k))  # perech var
                bools_list[i][j][k] = model.NewBoolVar(format_bool % (i, j, k))
    print("Declaring Variables Time: ", time() - now)
    now = time()

    """Sub-constraint for price """
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            for k in range(num_perech):
                # Adds an all-different constraint.
                model.Add(perech_list[i][j][k] <= req_qnty[i] ** 2).OnlyEnforceIf(bools_list[i][j][k])
                model.Add(perech_list[i][j][k] == 0).OnlyEnforceIf(bools_list[i][j][k].Not())

    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # Adds an all-different constrai12
            # Select one price per row of all perechs.
            # If one perech price is selected -> do not select other perech price variants
            for k in range(num_perech):
                # num of vars and bools in perech list (apprx 2 * 3=6)
                model.AddBoolAnd(list(map(lambda b: b.Not(),
                                          bools_list[i][j][:k] + bools_list[i][j][k + 1:]))
                                 ).OnlyEnforceIf(bools_list[i][j][k])
    print("Sub-constraint for price Time: ", time() - now)
    now = time()

    """Create Constr"""
    all_nals_list = []  # list of all sums of cash*cash_price of each product
    all_perechs_list = []  # list of all sums of perechs of each product
    all_perechs_list_prep_ratio = []  # list of all perech prices * prep_ratio  *qnty
    all_qnty_list = []  # sum of all qnty's per product

    # The sum of cols per price type constr
    for i in range(num_prod):
        # get column sum of cash*cash_price per each product
        all_nals_list.append(sum([cash_cost[i][j] * cash_list[i][j] for j in range(num_sup)]))
        # get column sum of perech*perech_price per each product
        all_perechs_list.append(sum([all_perechislenies[k][i][j] * perech_list[i][j][k]
                                     for k in range(num_perech)  # per item of perech ratio
                                     for j in range(num_sup)]))  # per supplier
        # get column sum of perech*perech_price*qnty*prep_ratio per each product
        all_perechs_list_prep_ratio \
            .append(sum([all_perechislenies_prep_ratio[k][i][j] * perech_list[i][j][k]
                         for k in range(num_perech)  # per item of perech ratio
                         for j in range(num_sup)]))  # per supplier
        # get column sum of cash and perech qnty per each product
        all_qnty_list.append(sum([
            cash_list[i][j] + sum(perech_list[i][j]) for j in range(num_sup)
        ]))
    print("Create Constr Time: ", time() - now)
    now = time()

    nal_sum = sum(all_nals_list)
    perech_sum = sum(all_perechs_list)
    perech_sum_prep_ratio = sum(all_perechs_list_prep_ratio)
    total_sum = nal_sum + perech_sum  # original prices
    total_sum_prep_ratio = nal_sum + perech_sum_prep_ratio  # prices with *prepayment ratio
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    model.Add(nal_sum <= cash)
    model.Add(perech_sum_prep_ratio <= perech)
    model.Add(total_sum_prep_ratio <= input_capital)
    for i in range(num_prod):
        model.Add(all_qnty_list[i] >= req_qnty[i])

    # this one maximizes differece between predop and input cash (naturally this gives priority to
    #   smaller predoplata prices,
    #   but later constraint): model.Minimize(total_sum) minimazes later total payment
    #   the lesser total payment means -> now choose higher predoplata % (lower prices for predoplata)
    model.Maximize(input_capital - total_sum_prep_ratio)
    model.Minimize(total_sum)

    print(">>>> SOLVING")
    print(">>>> itme Started: " + time.now())
    """Solve"""
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    # Print Solution
    print()
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@")
    print(">>>> itme Solved : " + time.now())
    if status != 4: return solver.StatusName(status)

    now = time()
    for i in range(num_prod):
        row = "P-%s -> \n\t" % str(i)
        for j in range(num_sup):
            row = row + "%2s -> " % str(supplier[j])
            row = row + "N(%s) " % str(solver.Value(cash_list[i][j]))
            row = row + "P(%s);\n\t" % "{}".format(", ").join((
                str(solver.Value(perech_list[i][j][k]))
                for k in range(num_perech)
            ))
        print(row)
    print("********")
    all_perechislenies = (np.array(all_perechislenies) / 100).astype(int).tolist()
    cash_cost = (np.array(cash_cost) / 100).astype(int).tolist()
    print("Printing Time: ", time() - now)
    now = time()

    result = {}
    for j in range(num_sup):  # per supplier
        supp_dict = {}
        prices_dict = {}
        perech_total_price, cash_total_price = 0, 0
        for k in range(num_perech):  # per perech
            prices_dict[prices_title[1][k]] = {}
            for i in range(num_prod):  # per product
                if solver.Value(perech_list[i][j][k]) == 0: continue
                prices_dict[prices_title[1][k]].update({product[i]: solver.Value(perech_list[i][j][k])})
                perech_total_price += all_perechislenies[k][i][j] * solver.Value(perech_list[i][j][k])
        prices_dict[prices_title[0]] = {}
        for i in range(num_prod):  # per product
            if solver.Value(cash_list[i][j]) == 0: continue
            prices_dict[prices_title[0]].update({product[i]: solver.Value(cash_list[i][j])})
            cash_total_price += cash_cost[i][j] * solver.Value(cash_list[i][j])
        supp_dict['prices'] = prices_dict
        supp_dict['total_price'] = cash_total_price + perech_total_price
        supp_dict['cash_price'] = cash_total_price
        supp_dict['prepayment_price'] = perech_total_price
        if cash_total_price == 0 and perech_total_price == 0: continue
        result[supplier[j]] = supp_dict
    print(result)
    print("Fitting to Dict Time: ", time() - now)
    now = time()
    return result
