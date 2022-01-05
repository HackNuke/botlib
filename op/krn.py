# This file is placed in the Public Domain.


"kernel"


import getpass
import os
import pwd


from .cfg import Cfg
from .evt import Event
from .fnc import format
from .prs import parse


class Cfg(Cfg):

    console = False
    debug = False
    index = 0
    name = "op"
    verbose = False
    wd = ""


def boot(txt):
    parse(Cfg, txt)
    Cfg.console = "c" in Cfg.opts
    Cfg.daemon = "d" in Cfg.opts
    Cfg.verbose = "v" in Cfg.opts
    print(format(Cfg))

def kcmd(o, txt):
    e = Event()
    e.channel = ""
    e.orig = repr(o)
    e.txt = txt
    o.handle(e)


def privileges(name=None):
    if os.getuid() != 0:
        return
    if name is None:
        try:
            name = getpass.getuser()
        except KeyError:
            pass
    try:
        pwnam = pwd.getpwnam(name)
    except KeyError:
        return False
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    os.umask(0o22)
    return True


def root():
    if os.geteuid() != 0:
        return False
    return True
