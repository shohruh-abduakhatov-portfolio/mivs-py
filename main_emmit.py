import asyncio
import logging

from modules.kinetic_core import Logger
from MIVSClient import MIVSClient


main_loop = asyncio.get_event_loop()

Logger.init(level=logging.DEBUG)


async def launch_mivs():
    mivs_exec = MIVSClient(main_loop)
    print(">>>launch_mivs: Start")
    mivs = await mivs_exec.get_optimized_prices(data={})
    print(">>> launch_mivs: Result received")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(mivs)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


main_loop.create_task(launch_mivs())
main_loop.run_forever()
