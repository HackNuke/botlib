# This file is placed in the Public Domain.


"object event"


from opr import Parsed
from otb import Obj

class Event(Parsed):

    def __init__(self, txt, orig=None, origin=None):
        Parsed.__init__(self, txt)
        self.channel = origin or ""
        self.orig = orig or ""
        self.origin = origin or ""
        self.result = []

    def bot(self):
        return Obj.byorig(self.orig)

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        assert self.orig
        for txt in self.result:
            Obj.say(self.orig, self.channel, txt)
