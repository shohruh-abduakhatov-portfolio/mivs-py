import asyncio

from src import mc_mics_v2 as mc_mivs


async def main():
    product = [6013, 6020]
    drug_qnty_req = [1, 5]
    input_capital = 1_000_000
    cash = int(input_capital * 0.5)  # 500_000 # 150_000
    perech = input_capital - cash
    supplier = [
        11,
        10
    ]
    cash_cost = [
        [1000000, 1000000],  # prod_A
        [1000000, 1000000]]  # prod_B
    pred_100 = [[27794, 27794],
                [11560, 11560]]  # prod_B
    pred_50 = [
        [1000000, 1000000],  # prod_A
        [1000000, 1000000]]  # prod_B
    pred_25 = [
        [1000000, 1000000],  # prod_A
        [1000000, 1000000]]  # prod_B
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
