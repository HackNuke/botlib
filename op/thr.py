# This file is placed in the Public Domain.


"object thread"


import threading
import types


class Thr(threading.Thread):

    def __init__(self, func, thrname, *args):
        super().__init__(None, func, thrname, args, {}, daemon=True)
        self.result = None

    def __iter__(self):
        return self

    def __next__(self):
        for key in dir(self):
            yield key

    def join(self, timeout=None):
        super().join(timeout)
        return self.result


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
    name = kwargs.get("name", getname(func))
    t = Thr(func, name, *args)
    t.start()
    return t
