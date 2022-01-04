# This file is placed in the Public Domain.


"object handler"


import queue
import time


from .cmd import Cmd
from .evt import Event
from .obj import Object
from .thr import launch


class Stop(Exception):

    pass


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.queue = queue.Queue()
        self.stopped = False

    def event(self, txt, origin=None):
        e = Event()
        e.orig = repr(self)
        e.origin = origin or "user@handler"
        e.txt = txt
        return e

    def handle(self, e):
        e.parse()
        f = Cmd.get(e.cmd)
        if f:
            f(e)
            e.show()
        e.ready()

    def loop(self):
        while not self.stopped:
            try:
                self.handle(self.poll())
            except Stop:
                break

    def poll(self):
        return self.queue.get()

    def put(self, e):
        self.queue.put_nowait(e)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped = True
        self.queue.put(None)


    def wait(self):
        while 1:
            time.sleep(1.0)
