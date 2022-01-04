# This file is placed in the Public Domain.


"object client"


from .bus import Bus


from . import Object


class Client(Object):

    def __init__(self):
        Object.__init__(self)
        Bus.add(self)

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
