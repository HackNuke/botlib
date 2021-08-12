# This file is placed in the Public Domain.

import time

from bot.obj import Db, fmt, fntime, listfiles
from bot.krn import find, kernel
from bot.spc import wd
from bot.tms import elapsed 

def __dir__():
    return ("fnd",)

def fnd(event):
    if not event.args:
        fls = listfiles(wd)
        if fls:
            event.reply(",".join([x.split(".")[-1].lower() for x in fls]))
        return
    otype = event.args[0]
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    got = False
    k = kernel()
    db = Db()
    for fn, o in find(otype, event.gets, event.index, event.timed):
        nr += 1
        txt = "%s %s" % (str(nr), fmt(o, args or o.keys(), skip=event.skip.keys()))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")
