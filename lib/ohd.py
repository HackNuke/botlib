# This file is placed in the Public Domain.


"object handler"


from obj import Object
from olp import Loop
from otb import Cmd, Obj


class Cfg(Object):

    pass


class Handler(Loop):

    def __init__(self):
        Loop.__init__(self)
        self.cfg = Cfg()
        Obj.add(self)

    def announce(self, txt):
        self.raw(txt)

    def handle(self, e):
        f = Cmd.get(e.cmd())
        if f:
            f(e)
            e.show()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
    