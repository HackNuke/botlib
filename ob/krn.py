# This file is placed in the Public Domain.

"kernel"

import inspect
import os
import pkgutil
import sys
import time
import ob.spc

from .bus import Bus
from .obj import Db, Default, List, O, Object, cdir, spl
from .prs import parse_txt
from .hdl import Dispatcher, Handler, Loop
from .thr import launch

class Cfg(Default):

    pass


class Kernel(Dispatcher, Loop):
    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.cmds = Object()
        self.classes = Object()
        self.names = List()
        self.register("cmd", self.handle)

    def add(self, func):
        n = func.__name__
        self.cmds[n] = func

    def boot(self, disk=False):
        self.parse_cli(disk)
        ob.spc.wd = ob.spc.wd or self.cfg.wd or None
        cdir(ob.spc.wd + os.sep)
        cdir(os.path.join(ob.spc.wd, "store", ""))
        self.cfg.wd = ob.spc.wd

    def cmd(self, clt, txt):
        if not txt:
            return
        Bus.add(clt)
        e = clt.event(txt)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def do(self, e):
        self.dispatch(e)

    def handle(self, hdl, obj):
        obj.parse()
        f = self.cmds.get(obj.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()

    def init(self, mns):
        for mn in spl(mns):
            if not "." in mn:
                mn = "botm.%s" % mn
            mod = sys.modules.get(mn, None)
            i = getattr(mod, "init", None)
            if i:
                if self.opts("v"):
                    self.error("run %s" % mn.name)
                launch(i, self)

    def introspect(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
                self.cmds[o.__name__] = o
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                self.classes[o.__name__] = o
                self.names.append(o.__name__.lower(), "%s.%s" % (o.__module__, o.__name__))

    def find(self, pkgs):
        res = {}
        for pn in spl(pkgs):
            p = pkgutil.get_loader(pn)
            if not p:
                continue
            if not p.is_package:
                self.introspect(p)
                return
            pp = os.path.dirname(p.path)
            for mn in pkgutil.walk_packages([pp,], pn + "."):
                zip = mn[0].find_module(mn[1])
                mod = zip.load_module(mn[1])
                self.introspect(mod)


    def opts(self, ops):
        for opt in ops:
            if opt in self.cfg.opts:
                return True
        return False

    def parse_cli(self, disk=False):
        o = Default()
        if disk:
            db = Db()
            oo = db.lastobject(self.cfg)
            if oo:
                o.update(oo)
        txt = " ".join(sys.argv[1:])
        if txt:
            parse_txt(o, txt)
        self.cfg.update(o)
        if o.sets:
            self.cfg.update(o.sets)

    @staticmethod
    def privileges(name=None):
        if os.getuid() != 0:
            return
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except (TypeError, KeyError):
                return
        if name is None:
            try:
                name = getpass.getuser()
            except (TypeError, KeyError):
                pass
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            return False
        try:
            os.chown(ob.spc.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        os.setgroups([])
        os.setgid(pwn.pw_gid)
        os.setuid(pwn.pw_uid)
        old_umask = os.umask(0o22)
        return True

    @staticmethod
    def root():
        if os.geteuid() != 0:
            return False
        return True

    def scan(self, pkgs=""):
        res = {}
        for pn in spl(pkgs):
            p = __import__("%s.all" % pn, None)
            if not p:
                continue
            for mn in pkgutil.walk_packages(p.__path__, pn + "."):
                if self.opts("v"):
                    self.error("loading %s" % mn.name)
                zip = mn[0].find_module(mn[1])
                mod = zip.load_module(mn[1])
                self.introspect(mod)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

class Client(Handler):
    def cmd(self, txt):
        k = kernel()
        return k.cmd(self, txt)

    def handle(self, e):
        k = kernel()
        k.put(e)


class Test(Handler):
    def handle(self, e):
        k = kernel()
        k.put(e)


k = None


def find(name, selector=None, index=None, timed=None):
    k = kernel()
    got = False
    db = Db()
    for n in k.names.get(name, [name,]):
        for fn, o in db.find(n, selector, index, timed):
            got = True
            yield fn, o
    if not got:
         return (None, None)


def kernel():
    if k: 
        return k
    return getattr(sys.modules["__main__"], "k", None)

    
def run(txt, p):
    class Out(Client):
        def raw(self, txt):
            p(txt)
    k = Kernel()
    k.scan("bot")
    c = Out()
    res = k.cmd(c, txt)
    return res
