"""
Multi-Constraint Multi-Item Vendor Selection
"""
from __future__ import print_function

import numpy as np
from ortools.sat.python import cp_model


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
               prices_title):
    all_perechislenies = [pred_100, pred_50, pred_25]
    model = cp_model.CpModel()
    # lengths
    num_prod = len(product)
    num_sup = len(supplier)
    num_perech = len(all_perechislenies)  # 3 apprx
    # empty product-supplier-cash-[perechs] dict
    product_constr = np.full(shape=(num_prod, num_sup, 2, 1), fill_value=0).tolist()

    """Declaring Variables"""
    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
            product_constr[i][j][0] = model.NewIntVar(0, req_qnty[i] ** 2, format_cash % (i, j, 0))  # cash var
            perech_tmp_list = []
            for k in range(num_perech):
                int_var = model.NewIntVar(0, req_qnty[i] ** 2, format_perech % (i, j, k))  # perech var
                bool_var = model.NewBoolVar(format_bool % (i, j, k))
                # Adds an all-different constraint.
                model.Add(int_var <= req_qnty[i] ** 2).OnlyEnforceIf(bool_var)
                model.Add(int_var == 0).OnlyEnforceIf(bool_var.Not())
                perech_tmp_list.append([int_var, bool_var])
            # Select one price per row of all perechs.
            # If one perech price is selected -> do not select other perech price variants
            for k_out in range(num_perech):  # len of perech list (3 apprx)
                # num of vars and bools in perech list (apprx 2 * 3=6)
                tmp = [perech_tmp_list[k_in][1] for k_in in range(len(perech_tmp_list))]
                tmp_filter = tmp[:k_out] + tmp[k_out + 1:]
                tmp_filter = list(map(lambda x: x.Not(), tmp_filter))

                model.AddBoolAnd(tmp_filter).OnlyEnforceIf(tmp[k_out])
            product_constr[i][j][1] = perech_tmp_list

    """Create Constr"""
    all_nals_list = []  # list of all sums of cash*cash_price of each product
    all_perechs_list = []  # list of all sums of perechs of each product
    all_qnty_list = []  # sum of all qnty's per product

    # The sum of cols per price type constr
    for i in range(num_prod):  # per drug
        # get column sum of cash*cash_price per each product
        all_nals_list.append(sum([cash_cost[i][j] * product_constr[i][j][0]
                                  for j in range(num_sup)]))
        # get column sum of perech*perech_price per each product
        all_perechs_list.append(sum([all_perechislenies[k][i][j] * product_constr[i][j][1][k][0]
                                     for k in range(num_perech)  # per item of perech ratio
                                     for j in range(num_sup)]))  # per supplier
        # get column sum of cash and perech qnty per each product
        all_qnty_list.append(sum([
            product_constr[i][j][0] + sum([product_constr[i][j][1][k][0] for k in range(num_perech)])
            for j in range(num_sup)]
        ))

    nal_sum = sum(all_nals_list)
    perech_sum = sum(all_perechs_list)
    total_sum = nal_sum + perech_sum

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    model.Add(nal_sum <= cash)
    model.Add(perech_sum <= perech)
    model.Add(total_sum  <= input_capital)
    for i in range(num_prod):
        model.Add(all_qnty_list[i] >= req_qnty[i])

    model.Maximize(input_capital - total_sum)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # model.Add((nal_sum + perech_sum) <= input_capital)
    # model.Add(nal_sum <= cash)
    # model.Add(perech_sum <= perech)
    # for i in range(num_prod):
    #     model.Add(all_qnty_list[i] >= req_qnty[i])
    #
    # # model.Add((sum(all_qnty_list) - sum(req_qnty)) >= 0)
    # """and should be maximized"""
    # # the density of total input capital should be as less(high difference and difference >= 0) as possible
    # # model.Minimize(sum(all_qnty_list) - sum(req_qnty))  # todo remove if not working as expected
    # model.Maximize(input_capital - (nal_sum + perech_sum))
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<..

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
    if status != 4: return
    for i in range(num_prod):
        row = "P-%s -> \n\t" % str(i)
        for j in range(num_sup):
            row = row + "%2s -> " % str(supplier[j])
            row = row + "N(%s) " % str(solver.Value(product_constr[i][j][0]))
            row = row + "P(%s);\n\t" % "{}".format(", ").join((
                str(solver.Value(product_constr[i][j][1][k][0]))
                for k in range(num_perech)
            ))
        print(row)
    print(">>> converting to dict ...")
    result = {}
    for j in range(num_sup):  # per supplier
        supp_dict = {}
        prices_dict = {}
        perech_total_price, cash_total_price = 0, 0
        for k in range(num_perech):  # per perech
            prices_dict[prices_title[1][k]] = {}
            for i in range(num_prod):  # per product
                if solver.Value(product_constr[i][j][1][k][0]) == 0: continue
                prices_dict[prices_title[1][k]].update({product[i]: solver.Value(product_constr[i][j][1][k][0])})
                perech_total_price += all_perechislenies[k][i][j] * solver.Value(product_constr[i][j][1][k][0])
        prices_dict[prices_title[0]] = {}
        for i in range(num_prod):  # per product
            if solver.Value(product_constr[i][j][0]) == 0: continue
            prices_dict[prices_title[0]].update({product[i]: solver.Value(product_constr[i][j][0])})
            cash_total_price += cash_cost[i][j] * solver.Value(product_constr[i][j][0])
        supp_dict['prices'] = prices_dict
        supp_dict['total_price'] = cash_total_price + perech_total_price
        supp_dict['cash_price'] = cash_total_price
        supp_dict['prepayment_price'] = perech_total_price
        if cash_total_price == 0 and perech_total_price == 0: continue
        result[supplier[j]] = supp_dict
    print(result)
    return result
