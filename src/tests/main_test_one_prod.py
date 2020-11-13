import asyncio
from time import time

import numpy as np

# from src import mc_mivs_v3 as mc_mivs
from src import mc_mivs_v5 as mc_mivs


async def main():
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
    min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()

    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
    discount_threshold = np.full(shape=(len(supplier)), fill_value=0)
    discount_percent = np.full(shape=(len(supplier)), fill_value=0)
    supp_overhead = np.full(shape=(len(supplier)), fill_value=10)
    supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()



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
                                min_sum_per_supplier=min_sum_per_supplier,
                                discount_threshold=discount_threshold,
                                discount_percent=discount_percent,
                                supp_overhead=supp_overhead)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
