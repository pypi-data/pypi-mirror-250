import asyncio
import copy
from multiprocessing import Process
import time
import inspect
from logging import Logger
from typing import Any


async def execute_func(func, *args, **kwargs):
    if func:
        ret = func(*args, **kwargs)
        if inspect.iscoroutine(ret):
            return await ret
        return ret
    return None


async def execute_func_safe(func, *args, **kwargs):
    try:
        return await execute_func(func, *args, **kwargs)
    except Exception as ex:
        return ex


class WorkerProcess(Process):

    def __init__(self, process_id: str, is_expired, message_queue, queue_lock,
                 handler, logger: Logger, params: dict = None, worker_params_builder=None, on_close=None,
                 retry_count: int = 0, on_failure=None):

        Process.__init__(self)
        self.is_expired = is_expired
        self.process_id = process_id
        self.message_queue = message_queue
        self.queue_lock = queue_lock
        self.logger = logger
        self.handler_params = params or {}
        self.worker_params_builder = worker_params_builder
        self.handler = handler
        self.on_close = on_close
        self.on_failure = on_failure
        self.retry_count = retry_count

    def run(self):
        self.logger.info(self.f("Starting"))
        start_time = time.time()

        asyncio.run(self.process_data())

        self.logger.info(self.f(f"Exiting in {round(time.time() - start_time, 4)} seconds"))

    async def process_data(self):
        params = copy.deepcopy(self.handler_params)
        await self._build_params(params)

        empty_queue_waiting_time = 0.1
        while not self.is_expired.value:
            data = await self.pull()
            if data is not None:
                self.logger.debug(self.f(f"processing {data}"))

                ex = None
                try:
                    await execute_func(self.handler, data, **params)
                except Exception as tex:
                    ex = tex
                    self.logger.exception(self.f(f"Worker error on data (retry={self.retry_count}): {data}"))

                if ex and self.retry_count > 0:
                    ex = None
                    for i in range(self.retry_count):
                        try:
                            await self.retry(data, params)
                            break
                        except Exception as tex:
                            ex = tex
                            self.logger.exception(self.f(f"Retry {i + 1} error on data {data}."))

                if ex and self.on_failure:
                    self.on_failure(data, ex)
                empty_queue_waiting_time = 0.1
            else:
                await asyncio.sleep(empty_queue_waiting_time)
                if empty_queue_waiting_time < 1:
                    empty_queue_waiting_time += 0.1

        await execute_func(self.on_close, **params)

    async def pull(self):
        start_acquire_time = time.time()
        sleep_time = 0.001
        while not self.queue_lock.acquire():
            await asyncio.sleep(sleep_time)
            if sleep_time < 0.1:
                sleep_time += 0.001

        acquire_time = time.time() - start_acquire_time
        if acquire_time > 1:
            self.logger.warning(self.f(f"acquire lock time: {acquire_time}"))

        if self.message_queue.empty():
            self.queue_lock.release()
            return None

        data = self.message_queue.get()
        self.queue_lock.release()
        return data

    async def _build_params(self, params: dict):
        built_params = await execute_func(self.worker_params_builder)
        if isinstance(built_params, dict):
            params.update(built_params)

    async def retry(self, data: Any, params: dict):
        self.logger.info(self.f(f"RETRY processing {data}"))

        await execute_func_safe(self.on_close, **params)

        await self._build_params(params)

        await execute_func(self.handler, data, **params)

    def f(self, msg):
        return f"{self.process_id}: {msg}"
