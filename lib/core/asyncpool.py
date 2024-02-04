#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import asyncio

class WorkItem:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.future = asyncio.Future()

class AsyncWorker:
    def __init__(self, pool):
        self.pool = pool
        self.fut = None
        self.is_running = False
        self.func = None
        self.args = None
        self.kwargs = None

    def start(self):
        self.fut = asyncio.ensure_future(self.run())

    async def stop(self, timeout=None):
        await asyncio.wait_for(self.fut, timeout)

    async def run(self):
        while True:
            item = await self.pool.work_queue.get()
            if item is None:
                break
            try:
                self.is_running = True
                self.func = item.func
                self.args = item.args
                self.kwargs = item.kwargs
                result = await item.func(*item.args, **item.kwargs)
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
        self.closed = False
        self.finish_left = num_workers

    async def submit(self, func, *args, **kwargs) -> asyncio.Future:
        if self.closed:
            raise RuntimeError('submit after shutdown')
        item = WorkItem(func, *args, **kwargs)
        await self.work_queue.put(item)
        return item.future

    async def shutdown(self, timeout=None, cancel_queued=False):
        self.closed = True
        if cancel_queued:
            while not self.work_queue.empty():
                item = await self.work_queue.get()
                if item:
                    item.future.set_exception(asyncio.CancelledError())
            await asyncio.sleep(0)

        while self.finish_left > 0:
            self.finish_left -= 1
            await self.work_queue.put(None)

        await asyncio.gather(
            *(worker.stop(timeout) for worker in self.workers), return_exceptions=True
        )

    @property
    def is_finished(self):
        return (not any(w.is_running for w in self.workers)) and self.work_queue.empty()


class PoolCollector:
    def __init__(self, pool: AsyncPool):
        self.pool = pool
        self.queue = asyncio.Queue()

    @classmethod
    def create(cls, num_workers, backlog=0):
        pool = AsyncPool(num_workers, backlog=backlog)
        return cls(pool)

    @property
    def remain_task_count(self):
        return self.pool.work_queue.qsize()

    @property
    def scanning_task_count(self):
        return len([w for w in self.pool.workers if w.is_running])

    @property
    def scanning_task_list(self):
        task_list = []
        for worker in self.pool.workers:
            if worker.args and worker.is_running:
                task_list.append(worker.args)
        return task_list


    async def submit(self, func, *args, **kwargs):
        future = await self.pool.submit(func, *args, **kwargs)
        future.add_done_callback(self.queue.put_nowait)
        return future

    async def submit_all(self, items):
        for item in items:
            await self.submit(item.func, *item.args, **item.kwargs)
        await self.shutdown()

    async def shutdown(self):
        await self.pool.shutdown()
        await self.queue.put(None)

    @property
    def is_finished(self):
        return self.pool.is_finished

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.pool.shutdown(timeout=0, cancel_queued=True)
        while not self.queue.empty():
            future = await self.queue.get()
            ignore_cancelled(future)

    async def iter(self):
        while True:
            item = await self.queue.get()
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
            pass
