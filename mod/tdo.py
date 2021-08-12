# This file is in the Public Domain.

"todo lists"

from ob.obj import Object
from ob.krn import find

class Todo(Object):
    def __init__(self):
        super().__init__()
        self.txt = ""


def dne(event):
    if not event.args:
        event.reply("dne <string>")
        return
    s = {"txt": event.args[0]}
    for fn, o in find("todo", s):
        o._deleted = True
        o.save()
        event.reply("ok")
        break


def tdo(event):
    if not event.rest:
        event.reply("tdo <txt>")
        return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
