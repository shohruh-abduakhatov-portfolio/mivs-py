from MIVSExecutor import MIVSExecutor
from modules.kinetic_core.AbstractClient import AbstractClient, rpc, lpc
from modules.kinetic_core.AbstractExecutor import executor


@executor(MIVSExecutor)
class MIVSClient(AbstractClient):
    @lpc
    async def get_optimized_prices_goapteka(self, data, flag=False):
        pass


    @lpc
    async def get_optimized_prices(self, data, flag=False):
        """
        :param data:
        {
            "supplier_id": {
             "products": {
                 "101": [{"product_id": 101, "price": {"wire100":10, "wire50": 11}, "exp": "2019-05", "qty": 100},
                     {"product_id": 101, "price": {"wire100":10, "wire50": 11}, "exp": "2018-05", "qty": 100}],
                 "114": [{"product_id": 114, "price": {"wire100":10, "wire50": 11}, "exp": "2019-05", "qty": 100},
                      {"product_id": 114, "price": {"wire100":10, "wire50": 11}, "exp": "2018-05", "qty": 100}],
                 "103": [{"product_id": 103, "price": {"wire100":10, "wire50": 11}, "exp": "2019-05", "qty": 100}],
             }, // список товаров
             "delivery_fixed":30000, // фиксированная цена доставки
             "delivery_percent": 0.2, // цена доставки в проценте от цена закупа
             "delivery_free_min_price": 20000, // минимальная цена для бесплатной доставки
             "load": 0.01, // нагрузка
             "discount": [{"from":3000, "percent": 0.05}, {"from":4000, "percent": 0.06}]
            },
            ...
        }
        basket = {"101": {"qty": 1000, "exp": "2019-02"}, "102": {"qty": 1500, "exp": "2019-02"}, "114": {"qty": 1000, "exp": "2019-02"}}
        :param flag:

        :return:
        optimized_prices = {
            SUPPLIER_ID: {
                'prices': {
                    PRICE_VERSION: {
                        PRODUCT_ID: QTY,
                        PRODUCT_ID: QTY,
                        ...
                    },
                    PRICE_VERSION: ...
                },
                'total_price': TOTAL_PRICE,
                'prepayment_price': PREPAYMENT_PRICE
            },
            SUPPLIER_ID: ...
        }
        """
