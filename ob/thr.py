# This file is placed in the Public Domain.


"object thread"


import queue
import threading
import types


errors = []


class Thr(threading.Thread):
    def __init__(self, func, *args, daemon=True):
        super().__init__(None, self.run, "", (), {}, daemon=daemon)
        self.name = getname(func)
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.result = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self.result

    def run(self):
        func, args = self.queue.get()
        self.setName(self.name)
        self.result = func(*args)


def getname(o):
    t = type(o)
    if isinstance(t, types.ModuleType):
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__
    return None


def launch(func, *args, **kwargs):
    t = Thr(func, *args)
    t.start()
    return t
