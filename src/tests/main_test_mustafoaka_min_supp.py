

import asyncio
from time import time
from src.data.data_mustafoaka_2 import test
import numpy as np

# from src import mc_mivs_v3 as mc_mivs
from src import mc_mics_v2 as mc_mivs


async def main():
    decimal = 100
    start = time()
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
    min_sum_per_supplier = test['min_sum_per_supplier']
    #
    cash_cost = (np.array(cash_cost) * decimal).astype(int).tolist()
    pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()
    pred_50 = (np.array(pred_50) * decimal).astype(int).tolist()
    pred_25 = (np.array(pred_25) * decimal).astype(int).tolist()
    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
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
                                min_sum_per_supplier=min_sum_per_supplier)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
