# This file is placed in the Public Domain.

import ob
import time

from ob.krn import find, kernel
from ob.tms import elapsed 

wd = ob.getwd()

def __dir__():
    return ("fnd",)

def fnd(event):
    if not event.args:
        fls = ob.listfiles(wd)
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
    for fn, o in find(otype, event.gets, event.index, event.timed):
        nr += 1
        txt = "%s %s" % (str(nr), ob.fmt(o, args or o.keys(), skip=event.skip.keys()))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - ob.fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")
