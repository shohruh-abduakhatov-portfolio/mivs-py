import asyncio


from src import mc_mivs
from src.tests.data_generator import generate_data_num_2

async def main():
    product, drug_qnty_req, input_capital, cash, perech, supplier,\
    cash_cost, pred_100, pred_50, pred_25 = generate_data_num_2()
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
    result


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
