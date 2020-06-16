# BOTLIB - the bot library !
#
# core data.

__version__ = 87

import inspect, os, sys, threading, time, _thread

from .obj import Cfg, Db, Object
from .flt import Fleet
from .hdl import Command, Handler
from .utl import elapsed, get_exception
from .usr import Users

starttime = time.time()

class ENOKERNEL(Exception):

    pass

class Cfg(Cfg):

    pass

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._prompted = threading.Event()
        self._prompted.set()
        self._ready = threading.Event()
        self._started = False
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)
        kernels.append(self)

    def announce(self, txt):
        pass
        
    def add(self, cmd, func):
        self.cmds[cmd] = func

    def dispatch(self, event):
        func = self.cmds.get(event.cmd, None)
        if func:
            try:
                func(event)
            except Exception as ex:
                print(get_exception())
                return
        event.show()
        event.ready()

    def ready(self):
        self._ready.set()

    def say(self, channel, txt):
        print(txt)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        self._ready.wait()

kernels = []

def get_kernel(nr=0, exception=False):
    try:
        k = kernels[nr]
    except IndexError:
        if exception:
            raise ENOKERNEL
        k = Kernel()
    return k
