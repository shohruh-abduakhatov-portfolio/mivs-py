import asyncio

from src import mc_mivs


async def main():
    product = ['10716', '10729']
    drug_qnty_req = [10, 15]
    input_capital = 100000000
    cash = 0
    perech = 100000000
    supplier = ['10']
    cash_cost = [[100000000], [100000000]]
    pred_100 = [[19980], [19586]]
    pred_50 = [[100000000], [100000000]]
    pred_25 = [[100000000], [100000000]]
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
