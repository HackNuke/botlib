# This file is placed in the Public Domain.


import time


from .bus import Bus
from .dpt import Dispatcher
from .lop import Loop
from .obj import Object, get
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
    name = ""
    systemd = False
    uuids = []
    verbose = False
    version = None


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
        self.stdin = None
        self.stdout = None
        self.stderr = None

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

    def direct(self, txt):
        if self.stdout:
            self.stdout.write(txt)
            self.stdout.write("\n")
            self.stdout.flush()

    def do(self, e):
        self.dispatch(e)

    def error(self, txt):
        if self.stderr:
            self.stderr.write(txt)
            self.stderr.write("\n")
            self.stderr.flush()

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
                self.log("init %s" % mn)
                if threaded:
                    launch(i)
                else:
                    i()

    def log(self, txt):
        if self.cfg.verbose:
            self.direct(txt)

    def opt(self, ops):
        if not self.opts:
            return False
        for opt in ops:
            if opt in self.opts:
                val = getattr(self.opts, opt, None)
                if val:
                    return True
        return False


    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
