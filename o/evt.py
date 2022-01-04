# This file is placed in the Public Domain.


"object event"


import threading


from .bus import Bus
from .dft import Default
from .prs import parse


class Event(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.channel = ""
        self.orig = ""
        self.origin = ""
        self.result = []

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self, txt=None):
        parse(self, txt or self.txt)

    def ready(self):
        self._ready.set()
      
    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        assert self.orig
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        return self.result
