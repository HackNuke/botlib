# This file is placed in the Public Domain.


import time


from .bus import Bus
from .dpt import Dispatcher
from .lop import Loop
from .obj import Object, get, update
from .prs import parse
from .tbl import Table


def __dir__():
    return (
        "Cfg",
        "Kernel",
        "k"
    )


class Cfg(Object):

    index = None
    mod = ""
    mask = 0o22
    uuids = []


class Kernel(Bus, Loop):

    def __init__(self):
        Bus.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.classes = Object()
        self.cmds = Object()
        self.opts = Object()
        self.prs = Object()
        Dispatcher.register(self, "cmd", self.handle)

    def addcmd(self, cmd):
        Table.add(cmd)
        self.cmds[cmd.__name__] = cmd


    def handle(self, obj):
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

    def init(self, mns, pn, threaded=False):
        Table.init(mns, pn, threaded)


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
        self.cfg.mask = 0o22

    def scan(self, skip=None):
        Table.scan(skip)


    def wait(self):
        while 1:
            time.sleep(5.0)


k = Kernel()
