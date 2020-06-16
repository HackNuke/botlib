# BOTLIB - the bot library !
#
#

from .obj import Object
from .dbs import Db

def __dir__():
    return ("Todo", 'done', 'todo')

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def todo(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.tdo.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    got = []
    db = Db()
    for todo in db.find("bot.tdo.Todo", selector):
        todo._deleted = True
        todo.save()
        event.reply("ok")
        break
