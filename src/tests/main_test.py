import asyncio
from time import time

from src.mc_mics_v2 import main as mc_main
from src.tests.test_data import *


async def main():
    start = time()
    decimal = 100
    # m_input_capital = int(input_capital * decimal)
    # m_cash = int(cash * decimal)
    # m_perech = int(perech * decimal)

    # m_cash_cost = (np.array(cash_cost) * decimal).astype(int).tolist()
    # m_pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()
    # m_pred_50 = (np.array(pred_50) * decimal).astype(int).tolist()
    # m_pred_25 = (np.array(pred_25) * decimal).astype(int).tolist()
    prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]

    result = await mc_main(product,
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


# /home/sa/Desktop/gotaxi/pharma/src/mivs/venv/bin/python /snap/pycharm-professional/127/helpers/pydev/pydevd.py --multiproc --qt-support=auto --client 127.0.0.1 --port 42301 --file /home/sa/Desktop/gotaxi/pharma/src/mivs/src/tests/main_test_1700.py
# pydev debugger: process 6265 is connecting
#
# Connected to pydev debugger (build 191.6605.12)
# prod:  1702
# supp:  6
# [###] Declaring Variables Time:  0.3879673480987549
