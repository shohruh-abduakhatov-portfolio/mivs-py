import asyncio

from src import mc_mivs_v5 as mc_mivs
from src.data.data_mustafoaka_2000 import test
import numpy as np


async def main():
    product = test['products']
    drug_qnty_req = test['drug_qty_req']
    input_capital = test['input_capital']
    cash = test['cash']
    perech = test['wire']
    supplier = test['suppliers']
    cash_cost = test['cash_cost']
    pred_100 = test['wire_100']
    pred_50 = test['wire_50']
    pred_25 = test['wire_25']
    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
    min_sum_per_supplier = [0] * len(pred_25[0])
    print("min_sum_per_supplier: ", min_sum_per_supplier)
    print("prod: ", len(product))
    print("supp: ", len(pred_25[0]))
    discount_threshold = np.full(shape=(len(supplier)), fill_value=0)
    discount_percent = np.full(shape=(len(supplier)), fill_value=0)

    result = await mc_mivs.main(product,
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
                                discount_threshold=discount_threshold.tolist(),
                                discount_percent=discount_percent.tolist())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # main()
