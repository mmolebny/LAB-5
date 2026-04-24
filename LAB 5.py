import threading
import time
import asyncio

class MyAbortController:
    def __init__(self):
        self.is_cancelled = False
    def abort(self):
        self.is_cancelled = True

class AsyncMapper:
    def __init__(self, data):
        self.data = data

    def map_sync(self, func):
        res = []
        for item in self.data:
            res.append(func(item))
        return res

    def map_with_callback(self, simple_func, on_finish):
        def worker():
            time.sleep(0.4)
            my_results = []
            for item in self.data:
                my_results.append(simple_func(item))
            on_finish(my_results)
        t = threading.Thread(target=worker)
        t.start()

    def map_promise(self, async_func):
        loop = asyncio.get_event_loop()
        f = loop.create_future()
        async def run_and_set():
            items = []
            for x in self.data:
                items.append(await async_func(x))
            f.set_result(items)
        asyncio.ensure_future(run_and_set())
        return f

    async def map_async(self, async_func):
        out = []
        for i in self.data:
            val = await async_func(i)
            out.append(val)
        return out

    async def map_with_abort(self, async_func, controller):
        temp = []
        for item in self.data:
            if controller.is_cancelled:
                return temp
            temp.append(await async_func(item))
        return temp

async def slow_func(n):
    await asyncio.sleep(0.1)
    return n * 5

async def run_demo():
    mapper = AsyncMapper([1, 2, 3])
    print(await mapper.map_async(slow_func))