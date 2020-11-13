import asyncio

from src import mc_mics_v2 as mc_mivs


async def main():
    product = ["drug_A"]
    drug_qnty_req = [10]
    input_capital = 1_000_000_000_000
    cash = int(input_capital * 0.45)
    perech = input_capital - cash
    supplier = [
        "S1 ",
        "S2 "
    ]
    cash_cost = [
        [10, 8]
    ]
    pred_100 = [
        [10, 11]
    ]  # prod_B
    pred_50 = [
        [120, 92]
    ]
    pred_25 = [
        [12, 1]
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
