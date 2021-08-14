# This file is placed in the Public Domain.

"fnd locates objects"

import time

from .krn import find, kernel
from .obj import Db, fmt, fntime, listfiles, getwd
from .tms import elapsed 

wd = getwd()

def __dir__():
    return ("fnd",)

def fnd(event):
    """
    scans the datastore for matching objects

    :usage: fnd [<type>] [<key==val>|<key==val>]

    :param type: type of object
    :type type:  string

    without type a list of available types is shown

    :param key: key==value pair to match objects with
    :type key: string

    without a key==val all the objects of a type are returned

    :example: 1) fnd
    :example: 2) fnd cfg
    :example: 3) fnd cfg server==localhost

    """
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
