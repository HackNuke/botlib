# BOTLIB - Framework to program bots.
#
#

""" kernel code. """

import inspect
import logging
import sys
import threading
import time
import _thread

from . import Cfg, Db, cfg
from .csl import Console
from .flt import Fleet
from .hdl import Handler
from .shl import writepid
from .typ import get_name

import bot.lib

def __dir__():
    return ("Cfg", "Kernel")

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
        self.cfg = Cfg(cfg)
        self.db = Db()
        self.fleet = Fleet()
        self.force = False
        bot.lib.kernels.append(self)

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def cmd(self, txt):
        self.fleet.add(self)
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = "root@shell"
        e.parse()
        launch(dispatch, self, e)
        e.wait()
        return e
        
    def start(self, shell=False, init=True):
        if self.error:
            print(self.error)
            return False
        writepid()
        if cfg.root:
            self.cfg.last()
            self.cfg.txt = ""
            self.cfg.merge(cfg)
            self.cfg.save()
        else:
            self.cfg.merge(cfg)
        if self.cfg.owner:
            if not self.users.allowed(self.cfg.owner, "USER", log=False):
                self.users.meet(self.cfg.owner)
        if not self.cfg.modules:
            self.cfg.modules = "bot.mods"
        self.walk(self.cfg.modules, init)
        if shell:
            c = Console()
            c.cmds.update(self.cmds)
            c.start()
            self.fleet.add(c)
        super().start()
        return True

    def ready(self):
        self._ready.set()

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        logging.warning("waiting on %s" % get_name(self))
        self._ready.wait()
        logging.warning("shutdown")
