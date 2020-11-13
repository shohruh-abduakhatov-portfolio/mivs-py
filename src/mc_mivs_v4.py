"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function
from time import time
from ortools.sat.python import cp_model
import itertools
import numpy as np


_format = "%s_%s_%s"
format_cash = _format + "_cash"
format_cash_bool = _format + "_cash_bool"
format_perech = _format + "_perech"
format_bool = _format + "_bool"
format_ratio_sup = "%s_supp_ratio"


# converts list to np.array
def main(product,
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
         #  pred_50_prepay_ratio,
         #  pred_25_prepay_ratio,
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
    # pred_50_prepay_ratio_np = np.array(pred_50_prepay_ratio)
    # pred_25_prepay_ratio_np = np.array(pred_25_prepay_ratio)

    # remove to free up memmory
    del product, req_qnty, input_capital, cash, perech, supplier, cash_cost, pred_100, pred_50, pred_25, prices_title

    calc_mivs(product_np,
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
              #   pred_50_prepay_ratio_np,
              #   pred_25_prepay_ratio_np,
              min_sum_per_supplier=kwargs.get("min_sum_per_supplier"))


def remove_decimal_points(prices, input_capital, multiply_to=1, decimal=100):
    prices[prices == input_capital] = input_capital * (multiply_to + 1)
    res = (prices * decimal * multiply_to).astype(int)
    return res


def calc_mivs(product,
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
              # pred_50_prepay_ratio,
              # pred_25_prepay_ratio,
              **kwargs):
    all_time = time()
    # Do not remove below comment. Used for testing #### - OK
    pred_50_prepay_ratio = remove_decimal_points(pred_50, input_capital, multiply_to=0.5)
    pred_25_prepay_ratio = remove_decimal_points(pred_25, input_capital, multiply_to=0.25)
    _all = [cash_cost, pred_100, pred_50, pred_25]
    all_perechislenies = np.array([pred_100, pred_50, pred_25])
    all_perechislenies_prep_ratio = np.array([pred_100, pred_50_prepay_ratio, pred_25_prepay_ratio])
    min_sum_per_supplier = np.array(kwargs.get("min_sum_per_supplier"))

    # lengths - OK
    num_prod = len(product)
    num_sup = len(supplier)
    num_perech = len(all_perechislenies)  # 3 apprx

    # empty product-supplier-cash-[perechs] dict - OK
    model = cp_model.CpModel()
    cash_list = np.full(shape=(num_prod, num_sup, 1), fill_value=model.NewIntVar(0, 0, '_'))
    perech_list = np.full(shape=(num_prod, num_sup, num_perech), fill_value=model.NewIntVar(0, 0, '_'))
    bools_list = np.full(shape=(num_prod, num_sup, num_perech + 1), fill_value=model.NewIntVar(0, 0, '_'))
    ratio_per_supp_sum = np.full(shape=(num_sup), fill_value=model.NewIntVar(0, 0, '_'))

    """Declaring Variables - OK"""
    now = time()
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            cash_list[i, j, 0] = model.NewIntVar(0, req_qnty[i], format_cash % (i, j, 0))
            for k in range(num_perech):  # perech var
                perech_list[i, j, k] = model.NewIntVar(0, req_qnty[i], format_perech % (i, j, k))
                bools_list[i, j, k] = model.NewBoolVar(format_bool % (i, j, k))
            bools_list[i, j, num_perech] = model.NewBoolVar(format_cash_bool % (i, j, num_perech))

    # for multiplying this ratio (0 or 1) to total sum per supp - OK
    for j in range(num_sup):
        ratio_per_supp_sum[j] = model.NewIntVar(0, 1, format_ratio_sup % j)

    print("[###] Declaring Variables Time: ", time() - now)
    now = time()

    """Sub-constraint for price - OK"""
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            # print(j)
            # Adds an all-different constraint for cash.
            tmp_cash, tmp_bools, tmp_perechs = cash_list[i, j, 0], bools_list[i, j], perech_list[i, j]
            model.Add(tmp_cash == req_qnty[i]).OnlyEnforceIf(tmp_bools[-1])
            model.Add(tmp_cash == 0).OnlyEnforceIf(tmp_bools[-1].Not())
            for k in range(num_perech):
                # Adds an all-different constraint for perech and cash constr.
                model.Add(tmp_perechs[k] == req_qnty[i]).OnlyEnforceIf(tmp_bools[k])
                model.Add(tmp_perechs[k] == 0).OnlyEnforceIf(tmp_bools[k].Not())

    print("All Different")
    # Adds an all-different constrai12. Select one price per row of all perechs.
    # If one perech price is selected -> do not select other perech price variants
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            for k in range(num_perech + 1):
                # num of vars and bools in perech list (apprx 2 * 3=6)
                i_all_diff = np.delete(bools_list[:, j], k, 1).flatten()
                # for i_in in range(len(i_all_diff)):
                #     i_all_diff[i_in] = i_all_diff[i_in].Not()
                # model.AddBoolAnd(i_all_diff).OnlyEnforceIf(bools_list[i,j,k])

                # model.AddBoolAnd([i.Not() for i in np.delete(bools_list[:,j], k, 1).flatten()]).OnlyEnforceIf(bools_list[i,j,k])

    print("[###] Sub-constraint for price: ", time() - now)
    now = time()

    """Create Constr - OK """
    all_nals_list = cash_cost.flatten() * cash_list.flatten()  # list of all sums of cash*cash_price of each product

    all_perechislenies_reshaped = np.array(
        np.hsplit(all_perechislenies.T.reshape(num_sup, num_prod * num_perech), num_prod))
    all_perechs_list = (
                all_perechislenies_reshaped * perech_list).flatten()  # list of all sums of perechs of each product

    all_perechs_list_prep_ratio = (np.array(
        np.hsplit(all_perechislenies_prep_ratio.T.reshape(num_sup, num_prod * num_perech),
                  num_prod)) * perech_list).flatten()  # list of all perech prices * prep_ratio  *qnty
    all_qnty_list = np.sum(np.sum(cash_list, axis=1), axis=1) + np.sum(np.sum(perech_list, axis=1),
                                                                       axis=1)  # sum of all qnty's per product

    # all sums of costs per supplier (which is for minimum req sum per supplier)
    all_sums_per_sup_list = np.sum(all_nals_list.reshape(num_prod, num_sup).T, axis=1) + np.sum(
        np.sum(all_perechislenies_reshaped * perech_list, axis=2), axis=0)
    min_sum_per_supp_multip_by_ratio = min_sum_per_supplier * ratio_per_supp_sum

    nal_sum = np.sum(all_nals_list)
    perech_sum = np.sum(all_perechs_list)
    perech_sum_prep_ratio = np.sum(all_perechs_list_prep_ratio)
    total_sum = nal_sum + perech_sum  # original prices
    total_sum_prep_ratio = nal_sum + perech_sum_prep_ratio  # prices with *prepayment ratio
    print("[###] Create Constr: ", time() - now)
    print("total python time: ", time() - all_time)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> # Addditing actual constraints - OK
    now = time()
    model.Add(nal_sum <= cash)
    model.Add(perech_sum_prep_ratio <= perech)
    model.Add(total_sum_prep_ratio <= input_capital)
    for j in range(num_sup):
        model.Add(all_sums_per_sup_list[j] >= min_sum_per_supp_multip_by_ratio[j])
    model.Add(sum(all_sums_per_sup_list) == total_sum)
    for i in range(num_prod):
        model.Add(all_qnty_list[i] == req_qnty[i])
    model.Maximize(input_capital - total_sum_prep_ratio)
    model.Minimize(total_sum)
    print("Addditing actual constraints: ", time() - now)

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
    if status != 4:
        return solver.StatusName(status)

    # Print Results
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
    print("\n[###] Printing Time: ", time() - now)
    print()

    # Get values  to Dictionary
    now = time()
    result = {}
    for j in range(num_sup):  # per supplier
        supp_dict = {}
        prices_dict = {}
        perech_total_price, cash_total_price = 0, 0
        for k in range(num_perech):  # per perech
            prices_dict[prices_title[1][k]] = {}
            for i in range(num_prod):  # per product
                t = solver.Value(perech_list[i][j][k])
                if t == 0:
                    continue
                prices_dict[prices_title[1][k]].update({product[i]: t})
                perech_total_price += all_perechislenies[k][i][j] * t
        prices_dict[prices_title[0]] = {}
        for i in range(num_prod):  # per product
            l_cash = solver.Value(cash_list[i][j])
            if l_cash == 0:
                continue
            prices_dict[prices_title[0]].update({product[i]: l_cash})
            cash_total_price += cash_cost[i][j] * l_cash
        supp_dict['prices'] = prices_dict
        supp_dict['total_price'] = cash_total_price + perech_total_price
        supp_dict['cash_price'] = cash_total_price
        supp_dict['prepayment_price'] = perech_total_price
        if cash_total_price == 0 and perech_total_price == 0:
            continue
        result[supplier[j]] = supp_dict
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
                  min_sum_per_supplier=min_sum_per_supplier)