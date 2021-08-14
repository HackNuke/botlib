# This file is placed in the Public Domain.

"handler"

import queue
import threading

from .bus import Bus
from .err import Error, Restart, Stop
from .evt import Command, Event
from .obj import Object
from .thr import launch

class Dispatcher(Object):
    "dispatches to from event to callback"
    def __init__(self):
        super().__init__()
        self.cbs = Object()

    def dispatch(self, event):
        "use event.type to dispatch on."
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def register(self, name, callback):
        "register callback."
        self.cbs[name] = callback


class Loop(Object):
    "start/stop loop"
    def __init__(self):
        super().__init__()
        self.errorhandler = None
        self.queue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()

    def do(self, e):
        "the actual job todo."
        raise NotImplemented("do")

    def error(self, e):
        "call errorhandler"
        if self.errorhandler:
            self.errorhandler(e)

    def loop(self):
        "the loop itself."
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
        "restart loop"
        self.stop()
        self.start()

    def put(self, e):
        "put event to the loop."
        self.queue.put_nowait(e)

    def start(self):
        "start the loop thread."
        launch(self.loop)
        return self

    def stop(self):
        self.stopped.set()
        "stop the loop thread."
        self.queue.put(None)


class Handler(Dispatcher, Loop):
    "basic event handler class"
    def event(self, txt):
        "return event based on txt/"
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = Object.__dorepr__(self)
        return c

    def handle(self, e):
        "handle the event."
        raise NotImplemented("handle")

    def loop(self):
        "event handling loop."
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
        "return an event to proces."
        return self.queue.get()

    def raw(self, txt):
        "print txt, default is disabled"
        raise ENOTIMPLEMENTED("raw")

    def say(self, channel, txt):
        "relay to direct output"
        self.raw(txt)

    def start(self):
        "add handler to bus and start event loop."
        super().start()
        Bus.add(self)

