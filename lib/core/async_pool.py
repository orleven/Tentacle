#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import asyncio
from lib.core.data import logger

class WorkItem:
    def __init__(self, _func, *args, **kwargs):
        self._func = _func
        self._args = args
        self._kwargs = kwargs

        self.future = asyncio.Future()


class AsyncWorker:
    def __init__(self, pool):
        self.pool = pool
        self.is_running = False

    def start(self):
        self._fut = asyncio.ensure_future(self.run())

    async def stop(self, timeout=None):
        await asyncio.wait_for(self._fut, timeout)

    async def run(self):
        while True:
            item = await self.pool.work_queue.get()
            if item == None:
                break
            try:
                self.is_running = True
                result = await item._func(*item._args, **item._kwargs)
                item.future.set_result(result)
            except Exception as ex:
                item.future.set_exception(ex)
            finally:
                self.is_running = False


class AsyncPool:
    def __init__(self, num_workers, backlog=0):
        self.num_workers = num_workers
        self.workers = []
        self.work_queue = asyncio.Queue(backlog)
        for _ in range(num_workers):
            worker = AsyncWorker(self)
            worker.start()
            self.workers.append(worker)
        self._closed = False
        self._finish_left = num_workers

    async def submit(self, _func, *args, **kwargs) -> asyncio.Future:
        if self._closed:
            raise RuntimeError('submit after shutdown')
        item = WorkItem(_func, *args, **kwargs)
        await self.work_queue.put(item)
        return item.future

    async def shutdown(self, timeout=None, cancel_queued=False):
        self._closed = True
        if cancel_queued:
            # cancel all existing tasks
            while not self.work_queue.empty():
                item = await self.work_queue.get()
                if item:
                    item.future.set_exception(asyncio.CancelledError())

            # explicit yield to wake up other putters
            await asyncio.sleep(0)

        # put finishing item
        # note that putting more than num_workers times may block shutdown forever
        while self._finish_left > 0:
            self._finish_left -= 1
            await self.work_queue.put(None)

        # wait workers to complete
        await asyncio.gather(
            *(worker.stop(timeout) for worker in self.workers), return_exceptions=True
        )

    @property
    def is_finished(self):
        return (not any(w.is_running for w in self.workers)) and self.work_queue.empty()


class PoolCollector:
    def __init__(self, pool: AsyncPool):
        self._pool = pool
        self._queue = asyncio.Queue()

    @classmethod
    def create(cls, num_workers, backlog=0):
        pool = AsyncPool(num_workers, backlog=backlog)
        return cls(pool)

    @property
    def remain_task_count(self):
        return self._pool.work_queue.qsize()

    @property
    def scanning_task_count(self):
        return len([w for w in self._pool.workers if w.is_running])

    async def submit(self, _func, *args, **kwargs):
        future = await self._pool.submit(_func, *args, **kwargs)
        future.add_done_callback(self._queue.put_nowait)
        return future

    async def submit_all(self, items):
        for item in items:
            await self.submit(item._func, *item._args, **item._kwargs)
        await self.shutdown()

    async def shutdown(self):
        await self._pool.shutdown()
        await self._queue.put(None)

    @property
    def is_finished(self):
        return self._pool.is_finished

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self._pool.shutdown(timeout=0, cancel_queued=True)
        while not self._queue.empty():
            future = await self._queue.get()
            ignore_cancelled(future)

    async def iter(self):
        while True:
            item = await self._queue.get()
            if item is not None:
                yield item
            else:
                break


def ignore_cancelled(future):
    if not future:
        return
    try:
        future.result()
    except Exception as ex:
        if not isinstance(ex, asyncio.CancelledError):
            logger.warning('future exception', exc_info=True)


async def finish_detect_daemon(manager: PoolCollector, time_interval=5):
    last_status = True
    while True:
        await asyncio.sleep(time_interval)
        this_status = bool(manager.is_finished)
        if last_status and this_status:
            await manager.shutdown()
            break

        last_status = this_status
