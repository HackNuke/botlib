# This file is placed in the Public Domain.


from .hdl import Handler
from .krn import k


def __dir__():
    return ("Client",)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        k.add(self)

    def handle(self, e):
        k.put(e)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
