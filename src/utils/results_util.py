

def print_results(res, solver):
    for i in range(res.get('num_prod')):
        row = "P-%s -> \n\t" % str(i+1)
        for j in range(res.get('num_sup')):
            row = row + "%2s -> " % str(res.get('_supplier')[j])
            row = row + "N(%s) " % str(solver.Value(res.get('var_cash_list')[i][j]))
            row = row + "P(%s);\n\t" % "{}".format(", ").join((
                str(solver.Value(res.get('var_wire_list')[i][j][k]))
                for k in range(res.get('num_perech'))
            ))
        print(row)



def to_dict(res, solver):
    result = {}
    total_cost = 0
    for j in range(res.get('num_sup')):  # per supplier
        supp_dict = {}
        prices_dict = {}
        perech_total_price, cash_total_price = 0, 0
        for k in range(res.get('num_perech')):  # per perech
            prices_dict[res.get('_prices_title')[1][k]] = {}
            for i in range(res.get('num_prod')):  # per product
                t = solver.Value(res.get('var_wire_list')[i][j][k])
                if t == 0:
                    continue
                prices_dict[res.get('_prices_title')[1][k]].update({res.get('_product')[i]: t})
                perech_total_price += res.get('_wires')[k][i][j] * t

        prices_dict[res.get('_prices_title')[0]] = {}
        for i in range(res.get('num_prod')):  # per product
            l_cash = solver.Value(res.get('var_cash_list')[i][j])
            if l_cash == 0:
                continue
            prices_dict[res.get('_prices_title')[0]].update({res.get('_product')[i]: l_cash})
            cash_total_price += res.get('_cash_cost')[i][j] * l_cash

        supp_dict['prices'] = prices_dict
        supp_dict['total_price'] = cash_total_price + perech_total_price
        supp_dict['cash_price'] = cash_total_price
        supp_dict['prepayment_price'] = perech_total_price
        if solver.BooleanValue(res.get('var_bool_disc_per_supp_sum')[j]):
            tcps = solver.Value(res.get('all_total_cost_per_supp')[j])
            supp_dict['discount'] = tcps - (tcps * res.get('_discount_percent')[j])
        else:
            supp_dict['discount'] = 0

        # todo supp_dict['discount'] = min_sum_discount_req[j]
        if cash_total_price == 0 and perech_total_price == 0:
            continue
        result[res.get('_supplier')[j]] = supp_dict
        total_cost += supp_dict['total_price']
    result['total_cost'] = total_cost
    return result


def print_results_100(res, solver):
    print_result = ""
    for i in range(res.get('num_prod')):
        row = "P-%s -> \n\t" % str(i + 1)
        for j in range(res.get('num_sup')):
            row = row + "%2s -> " % str(res.get('_supplier')[j])
            row = row + "W(%s) x %s;\n\t" % ("{}".format(", ").join((
                str(solver.Value(res.get('var_wire_list')[i][j][k]))
                for k in range(res.get('num_perech')))), res['_wires'][0][i][j])
        print(row)
        print_result += row
    with open("mivs_result.txt", "w") as text_file:
        text_file.write(print_result)


def to_dict_100(res, solver):
    result = {}
    total_cost = 0
    for j in range(res.get('num_sup')):  # per supplier
        supp_dict = {}
        prices_dict = {}
        perech_total_price, cash_total_price = 0, 0
        for k in range(res.get('num_perech')):  # per perech
            prices_dict['wire_100'] = {}
            for i in range(res.get('num_prod')):  # per product
                t = solver.Value(res.get('var_wire_list')[i][j][k])
                if t == 0:
                    continue
                prices_dict['wire_100'].update({res.get('_product')[i]: t})
                perech_total_price += res.get('_wires')[k][i][j] * t
        # prices_dict[res.get('_prices_title')[0]] = {}
        # for i in range(res.get('num_prod')):  # per product
        #     l_cash = solver.Value(res.get('var_cash_list')[i][j])
        #     if l_cash == 0:
        #         continue
        #     prices_dict[res.get('_prices_title')[0]].update({res.get('_product')[i]: l_cash})
        #     cash_total_price += res.get('_cash_cost')[i][j] * l_cash

        supp_dict['prices'] = prices_dict
        supp_dict['total_price'] = cash_total_price + perech_total_price
        supp_dict['cash_price'] = cash_total_price
        supp_dict['prepayment_price'] = perech_total_price
        # if solver.BooleanValue(res.get('var_bool_disc_per_supp_sum')[j]):
        #     tcps = solver.Value(res.get('all_total_cost_per_supp')[j])
        #     supp_dict['discount'] = tcps - (tcps * res.get('_discount_percent')[j])
        # else:
        #     supp_dict['discount'] = 0

        # todo supp_dict['discount'] = min_sum_discount_req[j]
        if cash_total_price == 0 and perech_total_price == 0:
            continue
        result[res.get('_supplier')[j]] = supp_dict
        total_cost += supp_dict['total_price']
    result['total_cost'] = total_cost
    return result