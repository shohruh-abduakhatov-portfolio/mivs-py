"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function

from time import time

import numpy as np
from ortools.sat.python import cp_model

from src.utils.results_util import print_results, to_dict


_format = "%s_%s_%s"
fmt_cash = _format + "_cash"
fmt_cash_bool = _format + "_cash_bool"
fmt_perech = _format + "_perech"
fmt_bool = _format + "_bool"
fmt_ratio_sup = "%s_supp_ratio"
fmt_bool_sup = "%s_supp_bool"
fmt_bool_disc = "%s_bool_disc"


"""converts list to np.array"""
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
               pred_50_prepay_ratio=None,
               pred_25_prepay_ratio=None,
               **kwargs):
    product_np = np.array(product)
    req_qnty_np = np.array(req_qnty)
    input_capital_np = np.array(input_capital)
    cash_np = np.array(cash)
    perech_np = np.array(perech)
    supplier_np = np.array(supplier)
    cash_cost_np = np.array(cash_cost)
    pred_100_np = np.array(pred_100)
    pred_50_np = np.array(pred_50)
    pred_25_np = np.array(pred_25)
    prices_title_np = prices_title
    pred_50_prepay_ratio_np = np.array(pred_50_prepay_ratio)
    pred_25_prepay_ratio_np = np.array(pred_25_prepay_ratio)
    discount_percent = np.array(kwargs.get("discount_percent")) / 100
    supp_overhead = np.array(kwargs.get("supp_overhead"))


    # remove to free up memmory
    del product, req_qnty, input_capital, cash, perech, supplier, cash_cost, pred_100, pred_50, pred_25, prices_title

    result = await calc_mivs(product_np,
                             req_qnty_np,
                             input_capital_np,
                             cash_np,
                             perech_np,
                             supplier_np,
                             cash_cost_np,
                             pred_100_np,
                             pred_50_np,
                             pred_25_np,
                             prices_title_np,
                             pred_50_prepay_ratio_np,
                             pred_25_prepay_ratio_np,
                             min_sum_per_supplier=kwargs.get("min_sum_per_supplier"),
                             discount_threshold=kwargs.get("discount_threshold"),
                             discount_percent=list(discount_percent),
                             supp_overhead=supp_overhead)
    return result


def remove_decimal_points(prices, input_capital, multiply_to=1, decimal=100):
    prices[prices == input_capital] = input_capital * (multiply_to + 1)
    res = (prices * multiply_to).astype(int)
    return res


async def calc_mivs(_product,
                    _req_qnty,
                    _input_capital,
                    _cash,
                    _perech,
                    _supplier,
                    _cash_cost,
                    _pred_100,
                    _pred_50,
                    _pred_25,
                    _prices_title,
                    _pred_50_prepay_ratio,
                    _pred_25_prepay_ratio,
                    **kwargs):
    all_time = time()
    # Do not remove below comment. Used for testing #### - OK
    _pred_50_prepay_ratio = remove_decimal_points(_pred_50, _input_capital, multiply_to=0.5)
    _pred_25_prepay_ratio = remove_decimal_points(_pred_25, _input_capital, multiply_to=0.25)
    _all = [_cash_cost, _pred_100, _pred_50, _pred_25]
    _wires = np.array([_pred_100, _pred_50, _pred_25])
    _wires_prep_ratio = np.array([_pred_100, _pred_50_prepay_ratio, _pred_25_prepay_ratio])
    _min_sum_per_supplier = np.array(kwargs.get("min_sum_per_supplier"))
    _discount_threshold = np.array(kwargs.get("discount_threshold"))  # .astype(dtype=int)
    _discount_percent = np.array(kwargs.get("discount_percent")).astype(dtype=int)
    _supp_overhead = np.array(kwargs.get("supp_overhead")).astype(dtype=int)

    # lengths
    num_prod = len(_product)
    num_sup = len(_supplier)
    num_perech = len(_wires)  # 3 apprx

    # empty product-supplier-cash-[perechs] dict
    model = cp_model.CpModel()
    var_cash_list = np.full(shape=(num_prod, num_sup, 1), fill_value=model.NewIntVar(0, 0, '_'))
    var_wire_list = np.full(shape=(num_prod, num_sup, num_perech), fill_value=model.NewIntVar(0, 0, '_'))
    var_bool_list = np.full(shape=(num_prod, num_sup, num_perech + 1), fill_value=model.NewIntVar(0, 0, '_'))
    # var_ratio_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))
    var_bool_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))
    var_bool_disc_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))


    """Declaring Variables"""; print("[###] Declaring Variables: "); now = time()
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            var_cash_list[i, j, 0] = model.NewIntVar(0, _req_qnty[i], fmt_cash % (i, j, 0))
            for k in range(num_perech):  # perech var
                var_wire_list[i, j, k] = model.NewIntVar(0, _req_qnty[i], fmt_perech % (i, j, k))
                var_bool_list[i, j, k] = model.NewBoolVar(fmt_bool % (i, j, k))
            var_bool_list[i, j, num_perech] = model.NewBoolVar(fmt_cash_bool % (i, j, num_perech))

    for j in range(num_sup):
        # for multiplying this ratio (0 or 1) to total sum per supp
        # var_ratio_per_supp_sum[j] = model.NewIntVar(0, 1, fmt_ratio_sup % j)
        # discount bool for implying if sum_per_supp has exceeded given threshold
        var_bool_per_supp_sum[j] = model.NewBoolVar(fmt_bool_sup % j)
        var_bool_disc_per_supp_sum[j] = model.NewBoolVar(fmt_bool_disc % j)


    print(">>>> ", time() - now); now = time(); print()
    """Sub-constraint for price"""; print("[###] Sub-constraint for price")
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # Adds an all-different constraint for cash.
            tmp_cash, tmp_bools, tmp_perechs = var_cash_list[i, j, 0], var_bool_list[i, j], var_wire_list[i, j]
            model.Add(tmp_cash == _req_qnty[i]).OnlyEnforceIf(tmp_bools[-1])
            model.Add(tmp_cash == 0).OnlyEnforceIf(tmp_bools[-1].Not())
            for k in range(num_perech):
                # Adds an all-different constraint for perech.
                model.Add(tmp_perechs[k] == _req_qnty[i]).OnlyEnforceIf(tmp_bools[k])
                model.Add(tmp_perechs[k] == 0).OnlyEnforceIf(tmp_bools[k].Not())
            del tmp_cash, tmp_bools, tmp_perechs

    print("[###] All Different"); print("[###] Sub-constraint for price and All Different: ")

    # Adds an all-different constrai12. Select one price per row of all perechs.
    # If one perech price is selected -> do not select other perech price variants
    inv_bools_list = np.swapaxes(np.swapaxes(var_bool_list, 0, 1), 1, 2)
    for j in range(num_sup):  # per supplier
        for k in range(num_perech + 1):  # per prices (wire+cash)
            i_all_diff = np.delete(var_bool_list[:, j], k, 1).flatten()
            # num of vars and bools in perech list (apprx 2 * 3=6)
            for i_in in range(len(i_all_diff)):
                i_all_diff[i_in] = i_all_diff[i_in].Not()
            model.AddBoolAnd(i_all_diff).OnlyEnforceIf(var_bool_list[i, j, k])
            del i_all_diff
    del inv_bools_list, var_bool_list
    print(">>>> ", time() - now); now = time(); print()


    """Create Constr - OK """
    print("[###] Create Constr: ")
    all_cash_cost_list = _cash_cost.flatten() * var_cash_list.flatten()  # list of all sums of cash*cash_price of each product
    all_wires_reshaped = np.array(np.hsplit(_wires.T.reshape(num_sup, num_prod * num_perech), num_prod)) # W x P x S -> P x S x W
    all_wires_cost_list = (all_wires_reshaped * var_wire_list).flatten()  # list of all sums of perechs of each product
    # list of all perech prices * prep_ratio  *qnty
    all_wire_prep_ratio_cost_list = (np.array(
        np.hsplit(_wires_prep_ratio.T.reshape(num_sup, num_prod * num_perech), num_prod)
    ) * var_wire_list).flatten()
    # sum of all qnty's per product (sum of all vars for cash and wires as a result of combinatorics)
    all_qnty_list = np.sum(np.sum(var_cash_list, axis=1), axis=1) + np.sum(np.sum(var_wire_list, axis=1), axis=1)
    # all sums of costs per supplier (which is for minimum req sum per supplier)
    all_total_cost_per_supp = np.sum(all_cash_cost_list.reshape(num_prod, num_sup).T, axis=1) + \
                              np.sum(np.sum(all_wires_reshaped * var_wire_list, axis=2), axis=0)

    ### Min cost per supplier Loop
    for j in range(num_sup): # per supp
        bvpss = var_bool_per_supp_sum[j] # boolean_var_per_supplier_sum
        j_total_cost_per_supp = all_total_cost_per_supp[j]
        ### if all_total_cost_per_supp exceeds 0 val, var_bool_per_supp_sum = true
        model.Add(j_total_cost_per_supp > 0).OnlyEnforceIf(bvpss)
        model.Add(j_total_cost_per_supp == 0).OnlyEnforceIf(bvpss.Not())
        ### if var_bool_per_supp_sum = true, it means all_total_cost_per_supp should be greater than [equal to] _min_sum_per_supplier
        model.Add(j_total_cost_per_supp >= _min_sum_per_supplier[j]).OnlyEnforceIf(bvpss)
        model.Add(j_total_cost_per_supp == 0).OnlyEnforceIf(bvpss.Not())


    # Discount Loop
    # for j in range(num_sup):  # per supp
    #     bdps = bools_disc_per_supp_sum[j]  # boolean_discount_per_supplier
    #     # if bools_disc_per_supp_sum = true, total_sum_per_supp exceeds given threshold
    #     model.Add(all_sums_per_sup_list[j] >= discount_threshold[j]).OnlyEnforceIf(bdps)
    #     model.Add(all_sums_per_sup_list[j] != discount_threshold[j]).OnlyEnforceIf(bdps.Not())
    #     # if bools_disc_per_supp_sum = true, it means total_sum should be reduced
    #     model.Add(all_sums_per_sup_list[j] == all_sums_per_sup_list[j] - (
    #             all_sums_per_sup_list[j] * discount_percent[j])).OnlyEnforceIf(bdps)
    #     model.Add(all_sums_per_sup_list[j] == all_sums_per_sup_list[j]).OnlyEnforceIf(bdps.Not())

    # todo review 1.0
    # min_sum_per_supp_multiplied_by_ratio = _min_sum_per_supplier #* var_ratio_per_supp_sum

    cash_sum = np.sum(all_cash_cost_list)
    wire_sum = np.sum(all_wires_cost_list)
    wire_prep_ratio_sum = np.sum(all_wire_prep_ratio_cost_list)
    total_sum = cash_sum + wire_sum  # original prices
    total_prep_ratio_sum = cash_sum + wire_prep_ratio_sum  # prices with *prepayment ratio

    del all_wires_reshaped, all_wires_cost_list, all_wire_prep_ratio_cost_list
    print(">>>> ", time() - now); print()
    print("[###] total python time: "); print('>>>> ', time() - all_time); print()
    print("[###] Addditing actual constraints: "); now = time()


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> # Addditing actual constraints - OK


    model.Add(cash_sum <= _cash)
    model.Add(wire_prep_ratio_sum <= _perech)
    model.Add(total_prep_ratio_sum <= _input_capital)

    print('[###] per supp constr adding')
    # for j in range(num_sup):
    #     # todo review 1.1
    #     model.Add(all_total_cost_per_supp[j] >= min_sum_per_supp_multiplied_by_ratio[j])
    model.Add(sum(all_total_cost_per_supp) == total_sum) # todo review 1.2

    print('[###] qnty add const')
    for i in range(num_prod):
        model.Add(all_qnty_list[i] == _req_qnty[i])

    model.Maximize(_input_capital - total_prep_ratio_sum)
    model.Minimize(total_sum)
    model.Minimize(np.sum(all_total_cost_per_supp + _supp_overhead*var_bool_per_supp_sum))

    print(">>>> ", time() - now)
    print()
    print("[###] Del lists")  # to free-up memory
    print()
    print("~~~~~~~~~~~~~~~~ SOLVING ~~~~~~~~~~~~~~~~~")
    del all_qnty_list, total_prep_ratio_sum, all_cash_cost_list, \
        _pred_50_prepay_ratio, _pred_25_prepay_ratio, _all, _wires_prep_ratio, _min_sum_per_supplier#, \
        # min_sum_per_supp_multiplied_by_ratio, var_ratio_per_supp_sum


    """Solve"""
    solver = cp_model.CpSolver()
    # solver.parameters.num_search_workers = 7
    solver.parameters.num_search_workers = 2
    solver.parameters.max_time_in_seconds = 120.
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
        return status_dict

    """Print Results"""
    now = time()
    res = {
        "num_prod": num_prod,
        "num_sup": num_sup,
        "num_perech": num_perech,
        "_supplier": _supplier,
        "var_cash_list": var_cash_list,
        "var_wire_list": var_wire_list
    }
    print_results(res, solver)
    print("\n[###] Printing Time: ", time() - now)


    """Get values  to Dictionary"""
    now = time()
    _wires = (np.array(_wires) / 100).astype(int).tolist()
    _cash_cost = (np.array(_cash_cost) / 100).astype(int).tolist()
    res.update({
        '_prices_title': _prices_title,
        '_product': _product,
        '_wires': _wires,
        '_cash_cost': _cash_cost,
        'var_bool_disc_per_supp_sum': var_bool_disc_per_supp_sum,
        'all_total_cost_per_supp': all_total_cost_per_supp,
        '_discount_percent': _discount_percent
    })
    result = to_dict(res, solver)
    result.update(status_dict)
    print(result)
    print("\n[###] Fitting to Dict Time: ", time() - now)
    print("total time: ", time() - all_time)

    return result
    return None


if __name__ == "__main__":
    start = time()
    decimal = 100
    product = ["Product_1", "Product_2"]
    min_sum_per_supplier = [1, 2, 3, 1]
    drug_qnty_req = [10, 10]
    input_capital = 1500900000000
    cash = 150000
    perech = input_capital - cash
    supplier = ["S1",
                "S2",
                "S3",
                "S4"]
    cash_cost = [[400, 200, 150, 500], [400, 200, 150, 500]]
    pred_100 = [[440, 220, 165, 550], [400, 200, 150, 500]]
    pred_50 = [[400, 204, 153, 510], [400, 200, 7, 500]]
    pred_25 = [[420, 210, 158, 6], [5, 200, 150, 500]]
    disc_thresh = [0, 0, 0, 0]
    disc_perc = [0, 0, 0, 0]

    input_capital = int(input_capital * decimal)
    cash = int(cash * decimal)
    perech = int(perech * decimal)
    #
    cash_cost = (np.array(cash_cost) * decimal).astype(int).tolist()
    pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()
    pred_50 = (np.array(pred_50) * decimal).astype(int).tolist()
    pred_25 = (np.array(pred_25) * decimal).astype(int).tolist()
    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
    result = main(product,
                  drug_qnty_req,
                  input_capital,
                  cash,
                  perech,
                  supplier,
                  cash_cost,
                  pred_100,
                  pred_50,
                  pred_25,
                  prices_title,
                  None,
                  None,
                  min_sum_per_supplier=min_sum_per_supplier,
                  discount_threshold=disc_thresh,
                  discount_percent=disc_perc)
