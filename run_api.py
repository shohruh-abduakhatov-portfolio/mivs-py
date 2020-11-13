#!/usr/local/bin/python3.6

import asyncio
import json

import numpy as np
from quart import Quart, request


app = Quart(__name__)


# cache = None
# init_cache = None


@app.route('/get_optimal_prices', methods=['GET'])
async def get_optimal_prices():
    print("get_optimal_prices")
    product = json.loads(request.args.get('product'))
    drug_qnty_req = json.loads(request.args.get('drug_qnty_req'))
    input_capital = json.loads(request.args.get('input_capital'))
    cash = json.loads(request.args.get('cash'))
    perech = json.loads(request.args.get('perech'))
    supplier = json.loads(request.args.get('supplier'))
    prices_title = json.loads(request.args.get('prices_title'))

    preds = json.loads(request.args.get('preds')) # {"pred100": pred_100, "pred50": [], "pred25": []},)
    min_sum_per_supplier = json.loads(request.args.get('min_sum_per_supplier'))
    discount_threshold = json.loads(request.args.get('discount_threshold'))
    discount_percent = json.loads(request.args.get('discount_percent'))
    supp_overhead = json.loads(request.args.get('supp_overhead'))
    mivs_timeout = request.args.get('mivs_timeout', 280)
    num_workers = request.args.get('num_workers', 7)
    # from src import mc_mivs_v5_wire100 as mc_mivs
    from src import num1_mivs_wire100 as mc_mivs
    result = await mc_mivs.main(product,
                                drug_qnty_req,
                                input_capital,
                                cash,
                                perech,
                                supplier,
                                prices_title,
                                preds=preds,
                                min_sum_per_supplier=min_sum_per_supplier,
                                discount_threshold=discount_threshold,
                                discount_percent=discount_percent,
                                supp_overhead=supp_overhead,
                                mivs_timeout=mivs_timeout,
                                num_workers=num_workers)
    print("<<<")
    return json.dumps(result)


@app.route('/')
async def hello():
    return 'hello'


app.run()
