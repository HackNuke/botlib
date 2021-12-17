# This file is placed in the Public Domain.


from .evt import Event
from .lop import Loop


def __dir__():
    return ("Handler",)


class Handler(Loop):

    def cmd(self, txt):
        e = self.event(txt)
        self.do(e)
        e.wait()
        return e

    def event(self, txt, origin="root@shell"):
        c = Event()
        c.type = "cmd"
        c.txt = txt or ""
        c.orig = repr(self)
        c.origin = origin
        c.parse()
        return c

    def handle(self, e):
        self.put(e)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.event(self.poll()))

    def poll(self):
        return self.queue.get()
