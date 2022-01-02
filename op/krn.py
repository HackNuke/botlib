# This file is placed in the Public Domain.

"kernel"

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
