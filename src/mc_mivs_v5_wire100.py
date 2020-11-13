"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function

from time import time

import numpy as np
from ortools.sat.python import cp_model

from src.utils.results_util import print_results, to_dict, print_results_100, to_dict_100


_format = "%s_%s_%s"
fmt_cash = _format + "_cash"
fmt_cash_bool = _format + "_cash_bool"
fmt_perech = _format + "_perech"
fmt_bool = _format + "_bool"
fmt_ratio_sup = "%s_supp_ratio"
fmt_bool_sup = "%s_supp_bool"
fmt_bool_disc = "%s_bool_disc"


def remove_decimal_points(prices, input_capital, multiply_to=1, decimal=100):
    prices[prices == input_capital] = input_capital * (multiply_to + 1)
    res = (prices * multiply_to).astype(int)
    return res


async def main(_product,
               _req_qnty,
               _input_capital,
               _cash,
               _perech,
               _supplier,
               _prices_title,
               **kwargs):
    all_time = time()
    _pred_100 = kwargs['preds'].get('pred100')
    _all = [_pred_100]
    _wires = np.array([_pred_100])
    # _wires_prep_ratio = np.array([_pred_100])
    _min_sum_per_supplier = np.array(kwargs.get("min_sum_per_supplier"))
    _discount_threshold = np.array(kwargs.get("discount_threshold"))  # .astype(dtype=int)
    _discount_percent = np.array(kwargs.get("discount_percent")).astype(dtype=int)
    _supp_overhead = np.array(kwargs.get("supp_overhead")).astype(dtype=int)

    # lengths
    num_prod = len(_product)
    num_sup = len(_supplier)
    num_perech = len(_wires)  # 1 apprx

    # empty product-supplier-cash-[perechs] dict
    model = cp_model.CpModel()
    var_wire_list = np.full(shape=(num_prod, num_sup, num_perech), fill_value=model.NewIntVar(0, 0, '_'))
    var_bool_list = np.full(shape=(num_prod, num_sup, num_perech), fill_value=model.NewIntVar(0, 0, '_'))
    # var_ratio_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))
    var_bool_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))
    # var_bool_disc_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))

    """Declaring Variables"""
    print("[###] Declaring Variables: ")
    now = time()
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            for k in range(num_perech):  # perech var
                var_wire_list[i, j, k] = model.NewIntVar(0, _req_qnty[i], fmt_perech % (i, j, k))
                var_bool_list[i, j, k] = model.NewBoolVar(fmt_bool % (i, j, k))
            var_bool_per_supp_sum[j] = model.NewBoolVar(fmt_bool_sup % j)

    # for j in range(num_sup):
        # for multiplying this ratio (0 or 1) to total sum per supp
        # var_ratio_per_supp_sum[j] = model.NewIntVar(0, 1, fmt_ratio_sup % j)
        # discount bool for implying if sum_per_supp has exceeded given threshold
        # var_bool_per_supp_sum[j] = model.NewBoolVar(fmt_bool_sup % j)
        # var_bool_disc_per_supp_sum[j] = model.NewBoolVar(fmt_bool_disc % j)

    print(">>>> ", time() - now)
    now = time()
    print()
    """Sub-constraint for price"""
    print("[###] Sub-constraint for price")
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # Adds an all-different constraint for cash.
            # tmp_cash, tmp_bools, tmp_perechs = var_cash_list[i, j, 0], var_bool_list[i, j], var_wire_list[i, j]
            tmp_bools = var_bool_list[i, j]
            tmp_perechs = var_wire_list[i, j]
            for k in range(num_perech):
                # Adds an all-different constraint for perech.
                model.Add(tmp_perechs[k] == _req_qnty[i]).OnlyEnforceIf(tmp_bools[k])
                model.Add(tmp_perechs[k] == 0).OnlyEnforceIf(tmp_bools[k].Not())
            del tmp_bools, tmp_perechs

    print("[###] All Different")
    print("[###] Sub-constraint for price and All Different: ")

    # Adds an all-different constrai12. Select one price per row of all perechs.
    # If one perech price is selected -> do not select other perech price variants
    inv_bools_list = np.swapaxes(np.swapaxes(var_bool_list, 0, 1), 1, 2)
    for j in range(num_sup):  # per supplier
        for k in range(num_perech):  # per prices (wire100)
            i_all_diff = np.delete(var_bool_list[:, j], k, 1).flatten()
            # num of vars and bools in perech list (apprx 2 * 3=6)
            for i_in in range(len(i_all_diff)):
                i_all_diff[i_in] = i_all_diff[i_in].Not()
            model.AddBoolAnd(i_all_diff).OnlyEnforceIf(var_bool_list[i, j, k])
            del i_all_diff
    del inv_bools_list, var_bool_list
    print(">>>> ", time() - now)
    now = time()
    print()

    """Create Constr - OK """
    print("[###] Create Constr: ")
    # all_cash_cost_list = _cash_cost.flatten() * var_cash_list.flatten()  # list of all sums of cash*cash_price of each product
    all_wires_reshaped = np.array(
        np.hsplit(_wires.T.reshape(num_sup, num_prod * num_perech), num_prod))  # W x P x S -> P x S x W
    all_wires_cost_list = (all_wires_reshaped * var_wire_list).flatten()  # list of all sums of perechs of each product
    # list of all perech prices * prep_ratio  *qnty
    # all_wire_prep_ratio_cost_list = (np.array(
    #     np.hsplit(_wires_prep_ratio.T.reshape(num_sup, num_prod * num_perech), num_prod)
    # ) * var_wire_list).flatten()
    # sum of all qnty's per product (sum of all vars for cash and wires as a result of combinatorics)
    all_qnty_list = np.sum(np.sum(var_wire_list, axis=1), axis=1)
    # all sums of costs per supplier (which is for minimum req sum per supplier)
    all_total_cost_per_supp = np.sum(np.sum(all_wires_reshaped * var_wire_list, axis=2), axis=0)

    # Min cost per supplier Loop
    for j in range(num_sup):  # per supp
        bvpss = var_bool_per_supp_sum[j]  # boolean_var_per_supplier_sum
        j_total_cost_per_supp = all_total_cost_per_supp[j]
        # if all_total_cost_per_supp exceeds 0 val, var_bool_per_supp_sum = true
        model.Add(all_total_cost_per_supp[j] > 0).OnlyEnforceIf(bvpss)
        model.Add(all_total_cost_per_supp[j] == 0).OnlyEnforceIf(bvpss.Not())
        # if var_bool_per_supp_sum = true, it means all_total_cost_per_supp should be greater than [equal to] _min_sum_per_supplier
        model.Add(all_total_cost_per_supp[j] >= _min_sum_per_supplier[j]).OnlyEnforceIf(bvpss)
        model.Add(all_total_cost_per_supp[j] == 0).OnlyEnforceIf(bvpss.Not())

    # cash_sum = np.sum(all_cash_cost_list)
    wire_sum = np.sum(all_wires_cost_list)
    # wire_prep_ratio_sum = np.sum(all_wire_prep_ratio_cost_list)
    total_sum = wire_sum  # original prices
    # total_prep_ratio_sum = wire_prep_ratio_sum  # prices with *prepayment ratio

    del all_wires_reshaped, all_wires_cost_list  # , all_wire_prep_ratio_cost_list
    print(">>>> ", time() - now)
    print()
    print("[###] total python time: ")
    print('>>>> ', time() - all_time)
    print()
    print("[###] Addditing actual constraints: ")
    now = time()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> # Addditing actual constraints - OK

    # model.Add(cash_sum <= _cash)
    # model.Add(wire_prep_ratio_sum <= _perech)
    model.Add(total_sum <= _input_capital)

    print('[###] per supp constr adding')
    # for j in range(num_sup):
    #     # todo review 1.1
    #     model.Add(all_total_cost_per_supp[j] >= min_sum_per_supp_multiplied_by_ratio[j])
    model.Add(sum(all_total_cost_per_supp) == total_sum)  # todo review 1.2

    print('[###] qnty add const')
    for i in range(num_prod):
        model.Add(all_qnty_list[i] == _req_qnty[i])

    # model.Minimize(_input_capital - total_prep_ratio_sum)
    model.Minimize(total_sum)
    model.Minimize(np.sum(all_total_cost_per_supp + _supp_overhead))

    print()
    print("[###] Del lists")
    del all_qnty_list, _all, _min_sum_per_supplier  # , \
    # min_sum_per_supp_multiplied_by_ratio, var_ratio_per_supp_sum
    print(">>>> ", time() - now)

    print()
    print("~~~~~~~~~~~~~~~~ SOLVING ~~~~~~~~~~~~~~~~~")

    """Solve"""
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 2
    solver.parameters.max_time_in_seconds = 10.
    status = solver.Solve(model)

    """Print Solution"""
    print("~~~~~~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~~~~~~")
    print()
    print('  - status          : %s' % solver.StatusName(status), '(code:', status, ')')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    status_dict = {
        "status": solver.StatusName(status),
        "status_code": status
    }
    if status != 4:
        print('  - PROTO          : %s' % solver.ResponseProto())
        print('  - STATS          : %s' % solver.ResponseStats())
        print('  - STATS          : %s' % solver.BestObjectiveBound())

        return status_dict

    """Print Results"""
    now = time()
    res = {
        "num_prod": num_prod,
        "num_sup": num_sup,
        "num_perech": num_perech,
        "_supplier": _supplier,
        "var_wire_list": var_wire_list
    }
    print_results_100(res, solver)
    print("\n[###] Printing Time: ", time() - now)

    """Get values  to Dictionary"""
    now = time()
    _wires = (np.array(_wires) / 100).astype(int).tolist()
    # _cash_cost = (np.array(_cash_cost) / 100).astype(int).tolist()
    res.update({
        '_prices_title': _prices_title,
        '_product': _product,
        '_wires': _wires,
        'all_total_cost_per_supp': all_total_cost_per_supp,
        '_discount_percent': _discount_percent
    })
    result = to_dict_100(res, solver)
    result.update(status_dict)
    print(result)
    print("\n[###] Fitting to Dict Time: ", time() - now)
    print("total time: ", time() - all_time)

    return result
