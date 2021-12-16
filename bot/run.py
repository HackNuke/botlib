# This file is placed in the Public Domain.


import time


from .bus import Bus
from .dpt import Dispatcher
from .lop import Loop
from .obj import Object, get, update
from .prs import parse
from .tbl import Table
from .thr import launch
from .utl import spl

def __dir__():
    return (
        "Cfg",
        "Runtime",
    )


class Cfg(Object):

    console = False
    daemon = False
    debug = False
    index = None
    mod = ""
    mask = 0o22
    uuids = []
    verbose = False


class Runtime(Bus, Dispatcher, Loop):

    def __init__(self):
        Bus.__init__(self)
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.classes = Object()
        self.cmds = Object()
        self.opts = Object()
        self.prs = Object()
        self.register("cmd", self.handle)

    def addcmd(self, cmd):
        Table.add(cmd)
        self.cmds[cmd.__name__] = cmd

    def cmd(self, clt, txt):
        if not txt:
            return None
        e = clt.event(txt)
        e.origin = "root@shell"
        e.parse()
        self.do(e)
        e.wait()
        return None

    def do(self, e):
        self.dispatch(e)


    def handle(self, clt, obj):
        obj.parse()
        f = None
        mn = get(Table.modnames, obj.prs.cmd, None)
        if mn:
            mod = Table.get(mn)
            if mod:
                f = getattr(mod, obj.prs.cmd, None)
        if not f:
            f = get(self.cmds, obj.prs.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()

    def init(self, mns, threaded=False):
        for mn in spl(mns):
            mod = Table.get(mn)
            i = getattr(mod, "init", None)
            if i:
                if threaded:
                    launch(i)
                else:
                    i()

    def opt(self, ops):
        if not self.opts:
            return False
        for opt in ops:
            if opt in self.opts:
                val = getattr(self.opts, opt, None)
                if val:
                    return True
        return False


    def parse_cli(self, txt):
        parse(self.prs, txt)
        update(self.opts, self.prs.opts)
        update(self.cfg, self.prs.sets)
        self.cfg.index = self.prs.index
        self.cfg.console = self.opt("c")
        self.cfg.daemon = self.opt("d")
        self.cfg.debug = self.opt("z")
        self.cfg.mask = 0o22
        self.cfg.verbose = self.opt("v")


    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
