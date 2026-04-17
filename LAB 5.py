import threading
import time


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