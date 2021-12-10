# This file is placed in the Public Domain.


from .hdl import Handler
from .krn import getmain

def __dir__():
     return ("Client",)


class Client(Handler):

    def handle(self, clt, e):
        k = getmain("k")
        k.put(self, e)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
