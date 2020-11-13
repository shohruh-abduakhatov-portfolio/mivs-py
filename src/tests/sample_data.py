optimized_prices = \
    {
        1: {  # SUPPLIER_ID
            "prices": {
                "v_price_1": {
                    "p_id_1": 10,  # QTY
                    "p_id_2": 10,
                    "p_id_2": 10,
                },
                "v_price_2": {
                    "p_id_1": 10,
                    "p_id_2": 10,
                    "p_id_2": 10,
                }
            },
            'total_price': 100000,
            'prepayment_price': 25000
        },
        2: {
            "prices": {
                "v_price_1": {
                    "p_id_1": 10,
                    "p_id_2": 10,
                    "p_id_2": 10,
                },
                "v_price_2": {
                    "p_id_1": 10,
                    "p_id_2": 10,
                    "p_id_2": 10,
                }
            },
            'total_price': 100000,
            'prepayment_price': 25000
        }
    }

basket_pricelist = \
    {
        "supplier_id_1": {
            "products": {
                "101": [{"product_id": 101, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100},
                        {"product_id": 101, "price": {"wire100": 10, "wire50": 11}, "exp": "2018-05",
                         "qty": 100}],
                "114": [{"product_id": 114, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100},
                        {"product_id": 114, "price": {"wire100": 10, "wire50": 11}, "exp": "2018-05",
                         "qty": 100}],
                "103": [{"product_id": 103, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100}],
            },  # список товаров
            "delivery_fixed": 30000,  # фиксированная цена доставки
            "delivery_percent": 0.2,  # цена доставки в проценте от цена закупа
            "delivery_free_min_price": 20000,  # минимальная цена для бесплатной доставки
            "load": 0.01,  # нагрузка
            "discount": [{"from": 3000, "percent": 0.05}, {"from": 4000, "percent": 0.06}]
        },
        "supplier_id_2": {
            "products": {
                "101": [{"product_id": 101, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100},
                        {"product_id": 101, "price": {"wire100": 10, "wire50": 11}, "exp": "2018-05",
                         "qty": 100}],
                "114": [{"product_id": 114, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100},
                        {"product_id": 114, "price": {"wire100": 10, "wire50": 11}, "exp": "2018-05",
                         "qty": 100}],
                "103": [{"product_id": 103, "price": {"wire100": 10, "wire50": 11}, "exp": "2019-05",
                         "qty": 100}],
            },  # список товаров
            "delivery_fixed": 30000,  # фиксированная цена доставки
            "delivery_percent": 0.2,  # цена доставки в проценте от цена закупа
            "delivery_free_min_price": 20000,  # минимальная цена для бесплатной доставки
            "load": 0.01,  # нагрузка
            "discount": [{"from": 3000, "percent": 0.05}, {"from": 4000, "percent": 0.06}]
        }
    },

basket = {"101": {"qty": 1000, "exp": "2019-02"}, "102": {"qty": 1500, "exp": "2019-02"},
          "114": {"qty": 1000, "exp": "2019-02"}}
