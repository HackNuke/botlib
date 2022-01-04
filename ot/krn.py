# This file is placed in the Public Domain.

"kernel"

import getpass
import os
import pwd

from .cmd import Cmd
from .cfg import Cfg
from .cls import Cls
from .dft import Default
from .evt import Event
from .prs import parse
from .tbl import Tbl


def boot(txt):
    cfg = Cfg()
    parse(cfg, txt)
    return cfg

    
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
    old_umask = os.umask(0o22)
    return True

def root():
    if os.geteuid() != 0:
        return False
    return True