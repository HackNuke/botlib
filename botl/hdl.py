# This file is placed in the Public Domain.

"handler"

import queue
import threading

from .bus import Bus
from .evt import Command, Event
from .obj import Object
from .thr import launch

class Dispatcher(Object):
    def __init__(self):
        super().__init__()
        self.cbs = Object()

    def dispatch(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def register(self, name, callback):
        self.cbs[name] = callback


class Loop(Object):
    def __init__(self):
        super().__init__()
        self.errorhandler = None
        self.queue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()

    def do(self, e):
        raise NotImplemented("do")

    def error(self, e):
        if self.errorhandler:
            self.errorhandler(e)

    def loop(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.do(e)
            except Restart:
                dorestart = True
                break
            except Stop:
                break
            except Exception as ex:
                e.type = "error"
                e.exc = ex
                self.error(e)
        if dorestart:
            self.restart()

    def restart(self):
        self.stop()
        self.start()

    def put(self, e):
        self.queue.put_nowait(e)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        launch(self.loop)
        return self

    def stop(self):
        self.stopped.set()
        self.queue.put(None)


class Handler(Dispatcher, Loop):

    def event(self, txt):
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = Object.__dorepr__(self)
        return c

    def handle(self, e):
        raise NotImplemented("handle")

    def loop(self):
        while not self.stopped.isSet():
            try:
                txt = self.poll()
            except (ConnectionRefusedError, ConnectionResetError) as ex:
                e = Error()
                e.exc = ex
                self.error(e)
                break
            if txt is None:
                e = Error()
                e.exc = Break
                self.error(e)
                break
            e = self.event(txt)
            if not e:
                e.type = "error"
                e.exc = Stop
                self.error(e)
                break
            self.handle(e)

    def poll(self):
        return self.queue.get()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        super().start()
        Bus.add(self)

