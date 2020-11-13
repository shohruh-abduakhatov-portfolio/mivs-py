import asyncio

from src import mc_mics_v2 as mc_mivs


async def main():
    product = ["9221", "11755"]
    drug_qnty_req = [10, 11]
    input_capital = 1000000
    cash = int(input_capital * 0.5)
    perech = input_capital - cash
    supplier = [
        "10"
    ]
    cash_cost = [
        [100000]
    ]
    pred_100 = [
        [255]
    ]  # prod_B
    pred_50 = [
        [100000]
    ]
    pred_25 = [
        [100000]
    ]

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
                                prices_title)

    # print("result: \n>>>", result)
    # print("_Execution Time: ", time() - start, ' (secs)')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
