# This file is placed in the Public Domain.

"timer"

import threading
import time

from .obj import Object
from .thr import getname, launch

class Timer(Object):
    "wait number of seconds"
    def __init__(self, sleep, func, *args, name=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = name or ""
        self.state = Object()
        self.timer = None

    def run(self):
        "run payload."
        self.state.latest = time.time()
        launch(self.func, *self.args)

    def start(self):
        "start the timer."
        if not self.name:
            self.name = getname(self.func)
        timer = threading.Timer(self.sleep, self.run)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        "stop the timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):
    def run(self):
        thr = launch(self.start)
        super().run()
        return thr

