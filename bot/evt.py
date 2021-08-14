# This file is placed in the Public Domain.

"events"

import threading

from .bus import Bus
from .obj import Default
from .prs import parse_txt

class Event(Default):
    "basic event class."
    def __init__(self):
        super().__init__()
        self.channel = None
        self.done = threading.Event()
        self.error = ""
        self.exc = None
        self.orig = None
        self.result = []
        self.thrs = []
        self.type = "event"
        self.txt = None

    def bot(self):
        "return matching bot."
        return Bus.byorig(self.orig)

    def parse(self):
        "parse the event."
        if self.txt is not None:
            parse_txt(self, self.txt)

    def ready(self):
        "flag events as ready."
        self.done.set()

    def reply(self, txt):
        "reply with text."
        self.result.append(txt)

    def say(self, txt):
        "say text to channel."
        Bus.say(self.orig, self.channel, txt.rstrip())

    def show(self):
        "show results."
        if self.exc:
            self.say(str(self.exc))
            return
        bot = self.bot()
        if not bot:
            raise NoBot(self.orig)
        if bot.speed == "slow" and len(self.result) > 3:
            Output.append(self.channel, self.result)
            self.say("%s lines in cache, use !mre" % len(self.result))
            return
        for txt in self.result:
            self.say(txt)

    def wait(self, timeout=1.0):
        "wait for event to finish."
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join(timeout)

class Error(Event):
    "error events"


class Command(Event):
    "event of type 'cmd'"
    def __init__(self):
        super().__init__()
        self.type = "cmd"
