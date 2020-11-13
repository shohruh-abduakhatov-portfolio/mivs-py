

import asyncio
from time import time
# from src.data.data_pharmav2_data import test
from src.data.data_mustafoaka_8 import test
import numpy as np

# from src import mc_mivs_v3 as mc_mivs


async def main():
    decimal = 100
    start = time()
    product = test['products']
    drug_qnty_req = test['drug_qty_req']
    supplier = test['suppliers']
    input_capital = test['input_capital']
    cash = test['cash']
    perech = test['wire']

    pred_100 = test['wire_100']

    min_sum_per_supplier = test['min_sum_per_supplier']
    supp_overhead = test['supp_overhead']
    #remove decimal points
    input_capital = int(input_capital * decimal)
    cash = int(cash * decimal)
    perech = int(perech * decimal)

    pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()


    min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()
    supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()

    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
    discount_threshold = test['discount_threshold']
    discount_percent = test['discount_percent']
    from src import num1_mivs_wire100 as mc_mivs
    result = await mc_mivs.main(product,
                                drug_qnty_req,
                                input_capital,
                                cash,
                                perech,
                                supplier,
                                prices_title,
                                preds={"pred100": pred_100, "pred50": [], "pred25": []},
                                min_sum_per_supplier=min_sum_per_supplier,
                                discount_threshold=discount_threshold,
                                discount_percent=list(np.array(discount_percent) / 100),
                                supp_overhead=supp_overhead)
    return result



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
