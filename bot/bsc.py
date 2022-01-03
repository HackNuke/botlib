# This file is placed in the Public Domain.


import threading
import time


from ol.bus import Bus
from ol.cfg import Cfg
from ol.cmd import Cmd
from ol.dbs import Db, fntime, save
from ol.dbs import find
from ol.dft import Default
from ol.fnc import format
from ol.obj import Object, get, keys, update, values
from ol.thr import getname
from ol.prs import elapsed


starttime = time.time()


def cmd(event):
    event.reply(",".join(sorted(Cmd.cmds)))
    

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(fmt(Obj.objs[str(index)]))
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([getname(o) for o in values(Obj.objs)]))


def fnd(event):
    if not event.args:
        db = Db()
        event.reply(",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        )
        return
    otype = event.args[0]
    nr = -1
    got = False
    for fn, o in find(otype):
        nr += 1
        txt = "%s %s" % (str(nr), format(o))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


def thr(event):
    result = []
    for t in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(t).startswith("<_"):
            continue
        o = Object()
        update(o, vars(t))
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = t.getName()
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
    event.reply(elapsed(time.time() - starttime))
