import asyncio
import copy
import logging
from multiprocessing import Manager
import time
from datetime import datetime
from typing import Any, Callable

from .worker_process import WorkerProcess


log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")


def setup_logger(
        name: str, file_path: str = "", file_log_level: int = logging.ERROR, console_log_level: int = logging.DEBUG
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(console_log_level)
    logger.addHandler(console_handler)

    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(file_log_level)
        logger.addHandler(file_handler)
    return logger


class ProcessQueueBase:
    def __init__(self, num_of_processes: int, worker: Callable = None, log_dir: str = "", worker_params: dict = None,
                 worker_params_builder: Callable = None, on_close_process: Callable = None, retry_count: int = 0,
                 on_failure: Callable = None, console_log_level: int = logging.INFO,
                 file_log_level: int = logging.ERROR, name: str = ""):

        queue_size = 3 * num_of_processes

        self.manager = Manager()
        self.work_queue = self.manager.Queue(queue_size)
        self.queue_lock = self.manager.Lock()
        self.is_expired = self.manager.Value("is_expired", False)
        self.name = name
        self.start_time = time.time()

        time_str = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        log_file_path = f"{log_dir + '/' if log_dir else ''}{time_str}.main.log"
        log_name = self.name + ".main" or "processq.main"
        self.logger = setup_logger(
            log_name, file_path=log_file_path, console_log_level=console_log_level, file_log_level=file_log_level
        )

        log_file_path = ""
        if log_dir:
            log_file_path = f"{log_dir}/{time_str}.{num_of_processes}_processes.log"
        log_name = self.name + ".processes" or "processq.processes"
        self.process_logger = setup_logger(
            log_name, file_path=log_file_path, console_log_level=console_log_level, file_log_level=file_log_level
        )

        # Save the settings for processes, so that we can recreate a process
        self.settings = {
            "worker": worker,
            "worker_params_builder": worker_params_builder,
            "on_close_process": on_close_process,
            "on_failure": on_failure,
            "retry_count": retry_count,
            "worker_params": worker_params if worker_params else {},
        }
        # Init processes
        self.processes = []
        for tid in range(num_of_processes):
            process = self.create_process(f"{self.name + '-' if self.name else ''}Process-{tid + 1}")
            self.processes.append(process)

    def stop(self):
        # Wait for queue to empty
        while not self.work_queue.empty():
            self.logger.debug(f"QSIZE: {self.work_queue.qsize()}")
            time.sleep(1)
            processes = [p for p in self.processes if p.is_alive()]
            if not processes:
                break
        self.logger.debug("Queue is empty")

        self.is_expired.value = True

        # Wait for all processes to complete
        for p in self.processes:
            p.join()
        self.logger.info(f"Exiting {self.name} Main in {round(time.time() - self.start_time, 4)} seconds")

    def create_process(self, process_id: str):
        handler = self.settings["worker"]
        worker_params_builder = self.settings["worker_params_builder"]
        on_close_process = self.settings["on_close_process"]
        retry_count = self.settings["retry_count"]
        worker_params = self.settings["worker_params"]
        on_failure = self.settings["on_failure"]
        params = copy.deepcopy(worker_params)
        process = WorkerProcess(process_id, self.is_expired, self.work_queue, self.queue_lock, handler,
                                self.process_logger, params=params, worker_params_builder=worker_params_builder,
                                on_close=on_close_process, retry_count=retry_count, on_failure=on_failure,
                                )
        process.start()
        return process

    def _wait_for_acquire_lock(self, waited_time: float = 0) -> float:
        acquire_waiting_time = waited_time + 0.0002
        if waited_time >= 0.1:
            acquire_waiting_time = 0.1
        if not self.queue_lock.acquire():
            return acquire_waiting_time
        return 0

    def _wait_for_not_full_queue(self, waited_time: float = 0) -> float:
        queue_full_waiting_time = waited_time + 0.01
        if waited_time >= 1:
            queue_full_waiting_time = 1
        if self.work_queue.full():
            self.queue_lock.release()
            return queue_full_waiting_time
        return 0


class SyncProcessQueue(ProcessQueueBase):
    def put(self, data: Any):
        qfull_waited_time = 0
        while True:
            wait_time = self._wait_for_acquire_lock()
            while wait_time > 0:
                time.sleep(wait_time)
                wait_time = self._wait_for_acquire_lock(wait_time)

            wait_time = self._wait_for_not_full_queue(qfull_waited_time)
            if wait_time > 0:
                time.sleep(wait_time)
                qfull_waited_time += wait_time
            else:
                break

        self.work_queue.put(data)
        self.queue_lock.release()


class AsyncProcessQueue(ProcessQueueBase):
    async def put(self, data: Any):
        qfull_waited_time = 0
        while True:
            wait_time = self._wait_for_acquire_lock()
            while wait_time > 0:
                await asyncio.sleep(wait_time)
                wait_time = self._wait_for_acquire_lock(wait_time)

            wait_time = self._wait_for_not_full_queue(qfull_waited_time)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                qfull_waited_time += wait_time
            else:
                break

        self.work_queue.put(data)
        self.queue_lock.release()


class ProcessQueue:

    def __init__(self, num_of_processes: int, worker: Callable = None, log_dir: str = "", worker_params: dict = None,
                 worker_params_builder: Callable = None, on_close_process: Callable = None, retry_count: int = 0,
                 console_log_level: int = logging.INFO, file_log_level: int = logging.ERROR, name: str = ""):
        self.init_params = {
            "num_of_processes": num_of_processes,
            "worker": worker,
            "log_dir": log_dir,
            "worker_params_builder": worker_params_builder,
            "worker_params": worker_params,
            "on_close_process": on_close_process,
            "retry_count": retry_count,
            "console_log_level": console_log_level,
            "file_log_level": file_log_level,
            "name": name,
        }

    def __enter__(self):
        self.instance = SyncProcessQueue(**self.init_params)
        return self.instance

    def __exit__(self, type, value, traceback):
        self.instance.stop()

    async def __aenter__(self):
        self.instance = AsyncProcessQueue(**self.init_params)
        return self.instance

    async def __aexit__(self, type, value, traceback):
        self.instance.stop()
