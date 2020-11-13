"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function

from time import time

import numpy as np
cimport numpy as np
from ortools.sat.python import cp_model
import itertools


### todo
#     6. Change Dictc return structure
ctypedef np.npy_float FLOAT
ctypedef np.npy_intp INTP

_format = "%s_%s_%s"
cdef str format_cash = _format + "_cash"
cdef str format_cash_bool = _format + "_cash_bool"
cdef str format_perech = _format + "_perech"
cdef str format_bool = _format + "_bool"
cdef str format_ratio_sup = "%s_supp_ratio"

def remove_decimal_points(prices, input_capital, multiply_to=1, decimal=100):
    tmp_prices = np.array(prices)
    tmp_prices[tmp_prices == input_capital] = input_capital * (multiply_to + 1)
    res = (tmp_prices * decimal * multiply_to).astype(int).tolist()
    return res

cdef dict main(list product,
               list req_qnty,
               int input_capital,
               int cash,
               int perech,
               list supplier,
               list cash_cost,
               list pred_100,
               list pred_50,
               list pred_25,
               list prices_title,
               #list list pred_50_prepay_ratio,
               #list pred_25_prepay_ratio,
               **kwargs):
    # Do not remove below comment. Used for testing ####
    pred_50_prepay_ratio = remove_decimal_points(pred_50, input_capital, multiply_to=0.5)
    pred_25_prepay_ratio = remove_decimal_points(pred_25, input_capital, multiply_to=0.25)

    model = cp_model.CpModel()
    cdef list all_perechislenies = list([pred_100, pred_50, pred_25])
    cdef list all_perechislenies_prep_ratio = list([pred_100, pred_50_prepay_ratio, pred_25_prepay_ratio])
    cdef list min_sum_per_supplier = kwargs.get("min_sum_per_supplier")
    # lengths
    cdef unsigned int num_prod, num_sup, num_perech = len(product), len(supplier), len(all_perechislenies)  # 3 apprx
    # empty product-supplier-cash-[perechs] dict
    cdef int cash_list[num_prod][num_sup][1][1]
    cdef int perech_list[num_prod][num_sup][1][1]
    cdef int bools_list[num_prod][num_sup][num_perech + 1][1]
    cdef int ratio_per_supp_sum[num_sup][1]
    cash_list = np.full(shape=(num_prod, num_sup, 1, 1), fill_value=0).tolist()
    perech_list = np.full(shape=(num_prod, num_sup, num_perech, 1), fill_value=0).tolist()
    bools_list = np.full(shape=(num_prod, num_sup, num_perech + 1, 1), fill_value=0).tolist()
    ratio_per_supp_sum = np.full(shape=(num_sup, 1), fill_value=0).tolist()

    """Declaring Variables"""
    now = time()
    cdef unsigned int i, j, k
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            cash_list[i][j] = model.NewIntVar(0, req_qnty[i], format_cash % (i, j, 0))  # todo
            for k in range(num_perech):
                perech_list[i][j][k] = model.NewIntVar(0, req_qnty[i], format_perech % (i, j, k))  # perech var
                bools_list[i][j][k] = model.NewBoolVar(format_bool % (i, j, k))
            bools_list[i][j][num_perech] = model.NewBoolVar(format_cash_bool % (i, j, num_perech))
    del i, j, k

    cdef unsigned int j
    for j in range(num_sup):
        ratio_per_supp_sum[j] = model.NewIntVar(0, 1, format_ratio_sup % j)
    del j

    print("[###] Declaring Variables Time: ", time() - now)
    now = time()

    """Sub-constraint for price """
    cdef unsigned int i, j, k
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # Adds an all-different constraint for cash.
            tmp_cash, tmp_bools, tmp_perechs = cash_list[i][j], bools_list[i][j], perech_list[i][j]
            model.Add(tmp_cash == req_qnty[i]).OnlyEnforceIf(tmp_bools[-1])
            model.Add(tmp_cash == 0).OnlyEnforceIf(tmp_bools[-1].Not())
            for k in range(num_perech):
                # Adds an all-different constraint for perech and cash constr.
                model.Add(tmp_perechs[k] == req_qnty[i]).OnlyEnforceIf(tmp_bools[k])
                model.Add(tmp_perechs[k] == 0).OnlyEnforceIf(tmp_bools[k].Not())
            del tmp_cash, tmp_bools, tmp_perechs
    del i, j, k
    print("[###] Sub-constraint for price Time: ", time() - now)
    now = time()

    cdef unsigned int i, j, k
    for i in range(num_prod):  # per drug
        print(i)
        for j in range(num_sup):  # per supplier
            # Adds an all-different constrai12. Select one price per row of all perechs.
            # If one perech price is selected -> do not select other perech price variants
            for k in range(num_perech + 1):
                # num of vars and bools in perech list (apprx 2 * 3=6)
                cdef unsigned int i_in
                cdef list same_sup_bools = list(itertools.chain(
                    *[bools_list[i_in][j][:k] + bools_list[i_in][j][k + 1:] for i_in in np.arange(num_prod).tolist()]))
                model.AddBoolAnd(list(map(lambda d: d.Not(), same_sup_bools))).OnlyEnforceIf(bools_list[i][j][k])
                del i_in
    del i, j, k
    print("[###] Create Constr Time: ", time() - now)
    print()
    now = time()

    """Create Constr"""
    cdef list all_nals_list = []  # list of all sums of cash*cash_price of each product
    cdef list all_perechs_list = []  # list of all sums of perechs of each product
    cdef list all_perechs_list_prep_ratio = []  # list of all perech prices * prep_ratio  *qnty
    cdef list all_qnty_list = []  # sum of all qnty's per product
    cdef list all_sums_per_sup_list = []  # all sums of costs per supplier (which is for minimum req sum per supplier)

    # The sum of cols per price type constr
    cdef unsigned int i
    for i in range(num_prod):
        cdef list tmp_perechs = perech_list[i]
        cdef list tmp_cash = cash_list[i]
        # get column sum of cash*cash_price per each product
        cdef unsigned int j
        all_nals_list.append(sum([cash_cost[i][j] * tmp_cash[j] for j in range(num_sup)]))
        del j
        # get column sum of perech*perech_price per each product
        cdef unsigned int j, k
        all_perechs_list.append(sum([all_perechislenies[k][i][j] * tmp_perechs[j][k]
                                     for k in range(num_perech)  # per item of perech ratio
                                     for j in range(num_sup)]))  # per supplier
        del j, k
        # get column sum of perech*perech_price*qnty*prep_ratio per each product
        cdef unsigned int j, k
        all_perechs_list_prep_ratio.append(sum([all_perechislenies_prep_ratio[k][i][j] * tmp_perechs[j][k]
                                                for k in range(num_perech)  # per item of perech ratio
                                                for j in range(num_sup)]))  # per supplier
        del j, k
        # get column sum of cash and perech qnty per each product
        cdef unsigned int j
        all_qnty_list.append(sum([
            tmp_cash[j] + sum(tmp_perechs[j]) for j in range(num_sup)
        ]))
        del j
    del i

    """create list of min sums requiremnt per supplier to buy"""
    cdef unsigned int j, i
    for j in range(num_sup):  # per supplier
        cdef unsigned int tmp_supp_sum = 0
        for i in range(num_prod):
            tmp_supp_sum += cash_list[i][j] * cash_cost[i][j]
            cdef unsigned int k
            tmp_supp_sum += sum([all_perechislenies[k][i][j] * perech_list[i][j][k] for k in
                                 range(num_perech)])  # per item of perech ratio
            del k
        # tmp_supp_sum *= ratio_per_supp_sum[j]
        all_sums_per_sup_list.append(tmp_supp_sum)
        del tmp_supp_sum
    del j, k

    cdef int nal_sum = sum(all_nals_list)
    cdef int perech_sum = sum(all_perechs_list)
    cdef int perech_sum_prep_ratio = sum(all_perechs_list_prep_ratio)
    cdef int total_sum = nal_sum + perech_sum  # original prices
    cdef int total_sum_prep_ratio = nal_sum + perech_sum_prep_ratio  # prices with *prepayment ratio
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    model.Add(nal_sum <= cash)
    model.Add(perech_sum_prep_ratio <= perech)
    model.Add(total_sum_prep_ratio <= input_capital)
    cdef unsigned int j, i
    for j in range(num_sup):
        model.Add(all_sums_per_sup_list[j] >= min_sum_per_supplier[j] * ratio_per_supp_sum[j])
    model.Add(sum(all_sums_per_sup_list) == total_sum)
    for i in range(num_prod):
        model.Add(all_qnty_list[i] == req_qnty[i])
    del i, j
    model.Maximize(input_capital - total_sum_prep_ratio)
    model.Minimize(total_sum)

    print(">>>> SOLVING")
    """Solve"""
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
    print("@@@@@@@@@@@@@@@@@@@@@@@")
    if status != 4: return solver.StatusName(status)

    now = time()
    for i in range(num_prod):
        _row = "P-%s -> \n\t" % str(i)
        cdef char *row = _row
        for j in range(num_sup):
            row = row + "%2s -> " % str(supplier[j])
            row = row + "N(%s) " % str(solver.Value(cash_list[i][j]))
            row = row + "P(%s);\n\t" % "{}".format(", ").join((
                str(solver.Value(perech_list[i][j][k]))
                for k in range(num_perech)
            ))
        print(row)
    print("********")
    # all_perechislenies = (np.array(all_perechislenies) / 100).astype(int).tolist()
    # cash_cost = (np.array(cash_cost) / 100).astype(int).tolist()
    # print("\n[###] Printing Time: ", time() - now)
    # print()
    # now = time()
    # 
    # result = {}
    # for j in range(num_sup):  # per supplier
    #     supp_dict = {}
    #     prices_dict = {}
    #     perech_total_price, cash_total_price = 0, 0
    #     for k in range(num_perech):  # per perech
    #         prices_dict[prices_title[1][k]] = {}
    #         for i in range(num_prod):  # per product
    #             t = solver.Value(perech_list[i][j][k])
    #             if t == 0: continue
    #             prices_dict[prices_title[1][k]].update({product[i]: t})
    #             perech_total_price += all_perechislenies[k][i][j] * t
    #     prices_dict[prices_title[0]] = {}
    #     for i in range(num_prod):  # per product
    #         l_cash = solver.Value(cash_list[i][j])
    #         if l_cash == 0: continue
    #         prices_dict[prices_title[0]].update({product[i]: l_cash})
    #         cash_total_price += cash_cost[i][j] * l_cash
    #     supp_dict['prices'] = prices_dict
    #     supp_dict['total_price'] = cash_total_price + perech_total_price
    #     supp_dict['cash_price'] = cash_total_price
    #     supp_dict['prepayment_price'] = perech_total_price
    #     if cash_total_price == 0 and perech_total_price == 0: continue
    #     result[supplier[j]] = supp_dict
    # print(result)
    # print("\n[###] Fitting to Dict Time: ", time() - now)
    return None  #result
