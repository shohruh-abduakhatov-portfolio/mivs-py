import json
from time import time

import numpy as np
import requests

from modules.kinetic_core.AbstractExecutor import AbstractExecutor
from src.tests.data_generator import *


class MIVSExecutor(AbstractExecutor):
    async def get_optimized_prices_original(self, data, flag=False):
        print("[###] input")
        print(data)
        print()
        if data == {}:
            product, drug_qnty_req, input_capital, \
            cash, perech, supplier, cash_cost, \
            pred_100, pred_50, pred_25 = generate_data_num_2()
            prices_title = ['cash', ['pred_100', 'pred_50', 'pred_25']]
        else:
            product = data['products']
            drug_qnty_req = data['drug_qty_req']
            supplier = data['suppliers']
            ## Uncomment later - multiply to 100 to remove double decimal position of the price (tiin)
            decimal = 100
            input_capital = int(data['input_capital'] * decimal)
            cash = int(data['cash'] * decimal)
            perech = int(data['wire'] * decimal)

            cash_cost = data['cash_cost']
            pred_100 = data['wire_100']
            pred_50 = data['wire_50']
            pred_25 = data['wire_25']

            min_sum_per_supplier = data['min_sum_per_supplier']
            supp_overhead = data['supp_overhead']
            # remove decimal points
            cash_cost = (np.array(cash_cost) * decimal).astype(int).tolist()
            pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()
            pred_50 = (np.array(pred_50) * decimal).astype(int).tolist()
            pred_25 = (np.array(pred_25) * decimal).astype(int).tolist()

            min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()
            supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()
            discount_threshold = data['discount_threshold']
            discount_percent = data['discount_percent']

            pred_50_prepay_ratio = self.remove_decimal_points(
                pred_50, data['input_capital'], multiply_to=0.5, decimal=0)
            pred_25_prepay_ratio = self.remove_decimal_points(
                pred_25, data['input_capital'], multiply_to=0.25, decimal=0)
            prices_title = ['cash_cost', self.get_wire_title_list_original(
                data)]  # prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]

        print(">>> received: ", time())
        from src import mc_mivs_v5 as mc_mivs
        # await asyncio.sleep()
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
                                    pred_50_prepay_ratio,
                                    pred_25_prepay_ratio,
                                    min_sum_per_supplier=min_sum_per_supplier,
                                    discount_threshold=discount_threshold,
                                    discount_percent=discount_percent,
                                    supp_overhead=supp_overhead)

        print(">>> r!!esult from executor")
        print(result)
        import copy
        result_ = {}
        for r in result:
            instance = result[r]
            instance_ = copy.deepcopy(instance)
            try:
                for p in instance["prices"]:
                    for pp in instance["prices"][p]:
                        instance_["prices"][p][str(pp)] = instance["prices"][p][pp]
                        pass
                        del instance_["prices"][p][pp]
            except:
                pass
            result_[str(r)] = instance_
        result = result_
        print(result)

        return result


    @staticmethod
    def get_wire_title_list_original(data):
        wire_title_list = list(filter(lambda x: x.startswith('wire_'), data.keys()))
        for i in range(len(wire_title_list)):
            wire_title_list[i] = wire_title_list[i].replace("_", "")
        wire_title_list.reverse()
        return wire_title_list


    async def get_optimized_prices_goapteka(self, data, flag=False):
        #return None
        print("[###] get_optimized_prices_goapteka")
        print(data)
        print()
        product = data['products']
        drug_qnty_req = data['drug_qty_req']
        supplier = data['suppliers']
        ## Uncomment later - multiply to 100 to remove double decimal position of the price (tiin)
        decimal = 100
        input_capital = int(data['input_capital'] * decimal)
        cash = int(data['cash'] * decimal)
        perech = int(data['wire'] * decimal)
        pred_100 = data.get('wire_100', [])
        min_sum_per_supplier = data['min_sum_per_supplier']
        supp_overhead = data['supp_overhead']

        # input_capital = int(input_capital * decimal)

        # remove decimal points
        pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()

        # aditional constrains
        min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()
        supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()
        discount_threshold = data['discount_threshold']
        discount_percent = data['discount_percent']
        mivs_timeout = data.get('mivs_timeout', 280)  # self.get_wire_title_list(data)
        num_workers = data.get('num_workers', 7)  # self.get_wire_title_list(data)
        prices_title = ['wire100']  # self.get_wire_title_list(data)

        print(">>> received: ", time())
        result = {}
        try:
            result = requests.get('http://127.0.0.1:5000/get_optimal_prices',
                                  params={
                                      "product": json.dumps(product),
                                      "drug_qnty_req": json.dumps(drug_qnty_req),
                                      "input_capital": json.dumps(input_capital),
                                      "cash": json.dumps(cash),
                                      "perech": json.dumps(perech),
                                      "supplier": json.dumps(supplier),
                                      "prices_title": json.dumps(prices_title),
                                      "preds": json.dumps({"pred100": pred_100, "pred50": [], "pred25": []}),
                                      "min_sum_per_supplier": json.dumps(min_sum_per_supplier),
                                      "discount_threshold": json.dumps(discount_threshold),
                                      "discount_percent": json.dumps(list(np.array(discount_percent) / 100)),
                                      "supp_overhead": json.dumps(supp_overhead),
                                      "mivs_timeout": mivs_timeout,
                                      "num_workers": num_workers
                                  },
                                  headers={
                                      "Accept": "application/json",
                                      "Content-type": "application/json"
                                  })
            result = json.loads(result.content)
        except:
            return "Empty"
        print(">>> r!!esult from executor")
        print(result)
        # import copy
        # result_ = {}
        # for r in result:
        #     instance = result[r]
        #     instance_ = copy.deepcopy(instance)
        #     try:
        #         for p in instance["prices"]:
        #             for pp in instance["prices"][p]:
        #                 instance_["prices"][p][str(pp)] = instance["prices"][p][pp]
        #                 pass
        #                 del instance_["prices"][p][pp]
        #     except:
        #         pass
        #     result_[str(r)] = instance_
        # result = result_
        return result


    async def get_optimized_prices(self, data, flag=False):
        print("[###] input")
        print(data)
        print()
        product = data['products']
        drug_qnty_req = data['drug_qty_req']
        supplier = data['suppliers']
        ## Uncomment later - multiply to 100 to remove double decimal position of the price (tiin)
        decimal = 100
        input_capital = int(data['input_capital'] * decimal)
        cash = int(data['cash'] * decimal)
        perech = int(data['wire'] * decimal)
        pred_100 = data.get('wire_100', [])
        min_sum_per_supplier = data['min_sum_per_supplier']
        supp_overhead = data['supp_overhead']

        # input_capital = int(input_capital * decimal)

        # remove decimal points
        pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()

        # aditional constrains
        min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()
        supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()
        discount_threshold = data['discount_threshold']
        discount_percent = data['discount_percent']

        prices_title = ['wire100']  # self.get_wire_title_list(data)

        print(">>> received: ", time())
        from src import mc_mivs_v5_wire100 as mc_mivs
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
        print(">>> r!!esult from executor")
        print(result)
        import copy
        result_ = {}
        for r in result:
            instance = result[r]
        instance_ = copy.deepcopy(instance)
        try:
            for p in instance["prices"]:
                for pp in instance["prices"][p]:
                    instance_["prices"][p][str(pp)] = instance["prices"][p][pp]
                    pass
                    del instance_["prices"][p][pp]
        except:
            pass
        result_[str(r)] = instance_
        result = result_
        return result


    async def get_optimized_prices_with_multi_prices(self, data, flag=False):
        print("[###] input")
        print(data)
        print()
        product = data['products']
        drug_qnty_req = data['drug_qty_req']
        supplier = data['suppliers']
        ## Uncomment later - multiply to 100 to remove double decimal position of the price (tiin)
        decimal = 100
        input_capital = int(data['input_capital'] * decimal)
        cash = int(data['cash'] * decimal)
        perech = int(data['wire'] * decimal)
        cash_cost = data.get('cash_cost', [])
        pred_100 = data.get('wire_100', [])
        pred_50 = data.get('wire_50', [])
        pred_25 = data.get('wire_25', [])
        min_sum_per_supplier = data['min_sum_per_supplier']
        supp_overhead = data['supp_overhead']

        # remove decimal points
        cash_cost = (np.array(cash_cost) * decimal).astype(int).tolist()
        pred_100 = (np.array(pred_100) * decimal).astype(int).tolist()
        pred_50 = (np.array(pred_50) * decimal).astype(int).tolist()
        pred_25 = (np.array(pred_25) * decimal).astype(int).tolist()
        pred_50_prep_ratio = self.remove_decimal_points(pred_50, data['input_capital'], multiply_to=0.5, decimal=0)
        pred_25_prep_ratio = self.remove_decimal_points(pred_25, data['input_capital'], multiply_to=0.25, decimal=0)

        # aditional constrains
        min_sum_per_supplier = (np.array(min_sum_per_supplier) * decimal).astype(int).tolist()
        supp_overhead = (np.array(supp_overhead) * decimal).astype(int).tolist()
        discount_threshold = data['discount_threshold']
        discount_percent = data['discount_percent']

        prices_title = self.get_wire_title_list(data)

        print(">>> received: ", time())
        from src import mc_mivs_v5_wire100 as mc_mivs
        result = await mc_mivs.main(product,
                                    drug_qnty_req,
                                    input_capital,
                                    cash,
                                    perech,
                                    supplier,
                                    cash_cost,
                                    prices_title,
                                    pred_prep_ratio={"pred_50_prep_ratio": pred_50_prep_ratio,
                                                     "pred_25_prep_ratio": pred_25_prep_ratio},
                                    preds={"pred100": pred_100, "pred50": pred_50, "pred25": pred_25},
                                    min_sum_per_supplier=min_sum_per_supplier,
                                    discount_threshold=discount_threshold,
                                    discount_percent=list(np.array(discount_percent) / 100),
                                    supp_overhead=supp_overhead)

        print(">>> r!!esult from executor")
        print(result)
        import copy
        result_ = {}
        for r in result:
            instance = result[r]
            instance_ = copy.deepcopy(instance)
            try:
                for p in instance["prices"]:
                    for pp in instance["prices"][p]:
                        instance_["prices"][p][str(pp)] = instance["prices"][p][pp]
                        pass
                        del instance_["prices"][p][pp]
            except:
                pass
            result_[str(r)] = instance_
        result = result_
        return result


    @staticmethod
    def remove_decimal_points(prices, input_capital, multiply_to=1, decimal=100):
        tmp_prices = np.array(prices)
        tmp_prices[tmp_prices == input_capital] = input_capital * (multiply_to + 1)
        res = (tmp_prices * decimal * multiply_to).astype(int).tolist()
        return res


    @staticmethod
    def get_wire_title_list(data):
        wire_title_list = list(filter(lambda x: x.startswith('wire_') or x.startswith('cash_cost'), data.keys()))
        for i in range(len(wire_title_list[1:])):
            wire_title_list[i] = wire_title_list[i].replace("_", "")
        wire_title_list.reverse()
        return wire_title_list
