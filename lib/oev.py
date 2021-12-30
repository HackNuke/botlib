# This file is placed in the Public Domain.


"object event"


from odf import Default
from opr import parse
from otb import Obj


class Event(Default):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.orig = ""
        self.origin = ""
        self.result = []

    def bot(self):
        return Obj.byorig(self.orig)

    def parse(self, txt=None):
        parse(self, txt or self.txt)
      
    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        assert self.orig
        for txt in self.result:
            Obj.say(self.orig, self.channel, txt)
