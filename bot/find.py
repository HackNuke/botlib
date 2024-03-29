# This file is placed in the Public Domain.


"find objects"


import time


from .command import Command
from .database import Db, fntime
from .database import find as fnd
from .function import format
from .parse import aliases, elapsed


def __dir__():
    return (
        "find",
    )


def find(event):
    if not event.args:
        db = Db()
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        if res:
            event.reply(res)
        return
    otype = event.args[0]
    nr = -1
    got = False
    for fn, o in fnd(otype):
        nr += 1
        txt = "%s %s" % (str(nr), format(o))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


Command.add(find)
aliases.fnd = "find"
