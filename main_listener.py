#!/usr/local/bin/python3.6

import os  # NOQA: E402
os.environ['VITA_CONFIG'] = '/var/www/config.py'  # NOQA: E402

import asyncio
import logging

from modules.kinetic_core import Logger
from modules.kinetic_core.AbstractExecutor import executor
from modules.kinetic_core.QueueListener import QueueListener
from MIVSExecutor import MIVSExecutor


main_loop = asyncio.get_event_loop()

Logger.init(level=logging.DEBUG)


# Регистрируем наш слушатель - он принимает сообщения из очереди rabbitMQ

@executor(MIVSExecutor)
class MIVSExecutorListener(QueueListener):
    async def parse(self, task):
        print('[###] mivs > start')
        await MIVSExecutor(task).parse()


main_loop.create_task(MIVSExecutorListener().register_listener(main_loop))
main_loop.run_forever()
