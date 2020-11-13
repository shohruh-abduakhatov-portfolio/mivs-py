import asyncio

from src import mc_mivs



async def main():
    product = ["drug_A"]
    drug_qnty_req = [10]
    input_capital = 1_000_000_000_000_000
    cash = int(input_capital * 0.15)
    perech = input_capital - cash
    supplier = [
        "P1",
        "P2",
        "P3",
        "P4",
        "P5",
        "P6",
        "P7",
        "P8",
        "P9",
        "P10",
        "P11",
        "P12",
        "P13",
        "P14",
        "P15",
        "P16",
        "P17",
    ]
    cash_cost = [[661096, 702645, 334348, 549022, 98971, 701367, 516241, 108871, 355646, 278511, 255499, 53295, 193850, 524844, 242727, 327308, 237079]]
    pred_100 = [[694150, 737777, 351065, 576473, 103919, 736435, 542053, 114314, 373428, 292436, 268273, 55959, 203542, 551086, 254863, 343673, 248932]]  # prod_B
    pred_50 = [[338811, 360105, 171353, 281373, 50722, 359450, 264573, 55796, 182268, 142736, 130943, 27313, 99348, 268982, 124397, 167745, 121502]]
    pred_25 = [[166926, 177417, 84422, 138628, 24990, 177095, 130350, 27489, 89800, 70324, 64513, 13456, 48947, 132523, 61288, 82645, 59862]]
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
