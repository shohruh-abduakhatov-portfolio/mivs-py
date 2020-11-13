import asyncio

from src import mc_mivs_v5 as mc_mivs
# from src.data.data_mustafoaka_2000 import test
from src.data.data_mustafoaka_3 import test


def increase_qny(lists, ratio=8):
    for i, o in enumerate(lists):
        lists[i] = o * ratio
    return lists

async def main():
    product = test['products']
    drug_qnty_req = test['drug_qty_req']
    input_capital = test['input_capital']
    cash = test['cash']
    perech = test['wire']

    supplier = test['suppliers'] * 8
    cash_cost = increase_qny(test['cash_cost'], 8)
    pred_100 = increase_qny(test['wire_100'], 8)
    pred_50 = increase_qny(test['wire_50'], 8)
    pred_25 = increase_qny(test['wire_25'], 8)
    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
    min_sum_per_supplier = [0] * len(pred_25[0])
    print("min_sum_per_supplier: ", min_sum_per_supplier)
    print("prod: ", len(product))
    print("supp: ", len(pred_25[0]))

    result = mc_mivs.main(product,
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # main()
