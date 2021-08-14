# This file is placed in the Public Domain.

"kernel"

import getpass
import inspect
import os
import pkgutil
import pwd
import sys
import time

from .bus import Bus
from .obj import Db, Default, List, O, Object, cdir, spl, getwd
from .prs import parse_txt
from .hdl import Dispatcher, Handler, Loop
from .thr import launch

class Cfg(Default):
    "kernel config"


class Kernel(Dispatcher, Loop):
    "the runtime kernel"
    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.cmds = Object()
        self.classes = Object()
        self.names = List()
        self.register("cmd", self.handle)

    def add(self, func):
        "add a command to the kernel."
        n = func.__name__
        self.cmds[n] = func

    def boot(self, disk=False):
        "set system paths."
        self.parse_cli(disk)
        wd = getwd() or self.cfg.wd or None
        cdir(wd + os.sep)
        cdir(os.path.join(wd, "store", ""))
        self.cfg.wd = wd

    def cmd(self, clt, txt):
        "execute a command and display on the client."
        if not txt:
            return
        Bus.add(clt)
        e = clt.event(txt)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def do(self, e):
        "dispatch to callbacks."
        self.dispatch(e)

    def error(self, e):
        "print error to stdout. defaults to off."

    def handle(self, hdl, obj):
        "check if there is a command, if so execute it and display results."
        obj.parse()
        f = self.cmds.get(obj.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()
 
    def init(self, mns):
        "initialise list of modules"
        for mn in spl(mns):
            if not "." in mn:
                mn = "botm.%s" % mn
            mod = sys.modules.get(mn, None)
            i = getattr(mod, "init", None)
            if i:
                if self.opts("v"):
                    self.error("init %s" % mn)
                launch(i, self)

    def introspect(self, mod):
        "scan module for commands and classes."
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
                self.cmds[o.__name__] = o
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                self.classes[o.__name__] = o
                self.names.append(o.__name__.lower(), "%s.%s" % (o.__module__, o.__name__))

    def opts(self, ops):
        "check commandline options."
        for opt in ops:
            if opt in self.cfg.opts:
                return True
        return False

    def parse_cli(self, disk=False):
        "parse command line options."
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
        "set privileges"
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
            os.chown(bot.spc.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        os.setgroups([])
        os.setgid(pwn.pw_gid)
        os.setuid(pwn.pw_uid)
        old_umask = os.umask(0o22)
        return True

    @staticmethod
    def root():
        "check if we are root."
        if os.geteuid() != 0:
            return False
        return True

    def scan(self, pkgs=""):
        "scan a package."
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
        "loop until end."
        while 1:
            time.sleep(5.0)

class Client(Handler):
    "basic client class"
    def cmd(self, txt):
        "run command through the kernel."
        k = kernel()
        return k.cmd(self, txt)

    def handle(self, e):
        "referer to the kernel."
        k = kernel()
        k.put(e)


class Test(Handler):
    "in case of tests."
    def handle(self, e):
        k = kernel()
        k.put(e)


#:
k = None


def find(name, selector=None, index=None, timed=None):
    "locate objects in store."
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
    "return the kernel."
    if k: 
        return k
    return getattr(sys.modules["__main__"], "k", None)

    
def run(txt, p, m):
    "run a command."
    class Out(Client):
        def raw(self, txt):
            p(txt)
    k = Kernel()
    k.scan(m)
    c = Out()
    res = k.cmd(c, txt)
    return res
