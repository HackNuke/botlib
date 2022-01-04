# This file is placed in the Public Domain.


"object client"


from .obj import Object


class Client(Object):

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)
