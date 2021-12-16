# This file is placed in the Public Domain.


from .dpt import Dispatcher
from .evt import Event
from .lop import Loop

def __dir__():
    return ("Handler",)


class Handler(Dispatcher, Loop):

    def __init__(self):
        Loop.__init__(self)
        Dispatcher.__init__(self)

    def event(self, txt, origin="root@shell"):
        c = Event()
        c.type = "cmd"
        c.txt = txt or ""
        c.orig = repr(self)
        c.origin = origin
        c.parse()
        return c

    def handle(self, e):
        Loop.put(e)

    def loop(self):
        while not self.stopped.isSet():
            try:
                self.handle(self.event(self.poll()))
            except Exception as ex:
                pass

    def poll(self):
        return self.queue.get()
