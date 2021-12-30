#!/usr/bin/env python3
# This file is placed in the Public Domain.


"object command"


import sys
import threading
import time


from obj import Object, get, keys, update
from odb import Cfg, find, fntime, listfiles, save
from odf import Default
from ofn import fmt
from otb import Cmd, Obj
from oth import getname

starttime = time.time()


def get_main(name):
    return getattr(sys.modules["__main__"], name, None)


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def cmd(event):
    
    event.reply(",".join(sorted(Cmd.cmds)))
    

def flt(event):
    try:
        index = int(event.args()[0])
        for o in Obj.objs:
            index -= 1
            if not index:
                event.reply(fmt(Obj.objs[str(index)], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([getname(o) for o in Obj.objs]))


def fnd(event):
    if not event.args():
        fls = listfiles(Cfg.wd)
        if fls:
            event.reply(",".join(sorted({x.split(".")[-1].lower()
                        for x in fls})))
        return
    otype = event.args()[0]
    nr = -1
    got = False
    for fn, o in find(otype):
        nr += 1
        txt = "%s %s" % (str(nr), fmt(o, keys(o)))
        if "-t" in event.txt:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


def log(event):
    print(event)
    if not event.rest():
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest()
    save(o)
    event.reply("ok")


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
