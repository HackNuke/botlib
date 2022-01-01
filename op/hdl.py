# This file is placed in the Public Domain.


"object handler"

from .bus import Bus
from .cmd import Cmd
from .obj import Object
from .lop import Loop


class Handler(Loop):

    def __init__(self):
        Loop.__init__(self)
        Bus.add(self)

    def announce(self, txt):
        self.raw(txt)

    def handle(self, e):
        e.parse()
        f = Cmd.get(e.cmd)
        if f:
            f(e)
            e.show()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
    