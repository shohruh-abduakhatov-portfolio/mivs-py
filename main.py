import asyncio
from time import time

import numpy as np

from src import mc_mivs
from src.utils import data_drug as data_param


async def main():
    start = time()
    ls_data = [
        data_param.producer,
        data_param.d9, data_param.d8, data_param.d7, data_param.d6, data_param.d5,
        data_param.d4, data_param.d3, data_param.d2, data_param.d1, data_param.dn
    ]

    requirement = [data_param.d9, data_param.d8, data_param.d7, data_param.d6, data_param.d5,
                   data_param.d4, data_param.d3, data_param.d2, data_param.d1, data_param.dn]

    req = np.array(requirement)
    # drugs_req = np.min(req, axis=1).tolist()
    drugs_req = [53295, 11253, 58945,  5415, 41635, 39815, 75205, 11722, 45855, 1]
    result = await mc_mivs.main(data=ls_data, nutrient=drugs_req)
    print(result)
    print("_Execution Time: ", time() - start, ' (secs)')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
