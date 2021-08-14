# This file is in the Public Domain.

"administrator"

import threading
import time

from .bus import Bus
from .krn import kernel
from .obj import Object, fmt
from .thr import getname
from .tms import elapsed

def __dir__():
    return ("flt", "thr", "upt")


k = kernel()
starttime = time.time()


def flt(event):
    "flt shows a list of bots"
    try:
        index = int(event.args[0])
        event.reply(fmt(Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))


def thr(event):
    "thr shows running threads"
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        o.update(vars(thr))
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s(%s)" % (txt, elapsed(up)))
    if res:
        event.reply(" ".join(res))


def upt(event):
    "upt shows the uptime"
    event.reply("uptime is %s" % elapsed(time.time() - starttime))
