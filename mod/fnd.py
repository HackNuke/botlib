# This file is placed in the Public Domain.

import os
import time

from obj import Names, fmt, find, listfiles, wd
from run import opts
from tms import elapsed, fntime, todate

def register():
    Names.add(fnd)

def fnd(event):
    if not event.args:
        fls = listfiles(wd)
        if fls:
            event.reply(",".join([x.split(".")[-1].lower() for x in fls]))
        return
    name = event.args[0]
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    got = False
    otypes = Names.getnames(name, [])
    for t in otypes:
        for fn, o in find(t, event.gets, event.index, event.timed):
            nr += 1
            txt = "%s %s" % (str(nr), fmt(o, args or o.keys(), skip=event.skip.keys()))
            if opts("t") or "t" in event.opts:
                if "Date" in o.keys():
                    fn = os.sep.join(todate(o.Date).split())
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            got = True
            event.reply(txt)
    if not got:
        event.reply("no result")