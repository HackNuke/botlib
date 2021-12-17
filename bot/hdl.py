# This file is placed in the Public Domain.


import threading


from .krn import k
from .lop import Loop
from .obj import Object
from .opt import Output
from .prs import parse as pparse


def __dir__():
    return ("Event", "Handler", "event", "cmd")


class Event(Object):

    def __init__(self):
        super().__init__()
        self.channel = None
        self.done = threading.Event()
        self.orig = None
        self.origin = None
        self.prs = Object()
        self.result = []
        self.type = "event"
        self.txt = None

    def bot(self):
        return k.byorig(self.orig)

    def parse(self):
        pparse(self.prs, self.txt)

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def say(self, txt):
        k.say(self.orig, self.channel, txt)

    def show(self):
        bot = self.bot()
        if bot.speed == "slow" and len(self.result) > 3:
            Output.append(self.channel, self.result)
            self.say("%s lines in cache, use !mre" % len(self.result))
            return
        for txt in self.result:
            self.say(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)


class Handler(Loop):


    def handle(self, e):
        self.put(e)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(event(self.poll(), repr(self)))

    def poll(self):
        return self.queue.get()


def event(txt, orig=None, origin="root@shell"):
    c = Event()
    c.type = "cmd"
    c.txt = txt or ""
    c.orig = orig
    c.origin = origin
    c.parse()
    return c


def cmd(clt, txt):
    e = event(txt, repr(clt))
    k.do(e)
    e.wait()
    return e
