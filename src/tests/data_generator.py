from . import test_data as data


def generate_data_num_2():
    product = data.product[:2]
    drug_qnty_req = data.drug_qnty_req[:2]
    input_capital = data.input_capital
    cash = data.cash
    perech = data.perech
    supplier = data.supplier
    cash_cost = data.cash_cost[:2]
    pred_100 = data.pred_100[:2]
    pred_50 = data.pred_50[:2]
    pred_25 = data.pred_25[:2]
    return product, drug_qnty_req, input_capital, cash, perech, supplier, cash_cost, pred_100, pred_50, pred_25
