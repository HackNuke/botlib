# This file is placed in the Public Domain


from .obj import Object, get
from .fnc import register


class Cmd(Object):

    cmd = Object()
    events = []

    @staticmethod
    def add(cmd):
        register(Cmd.cmd, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        f =  get(Cmd.cmd, cmd)
        return f


def dispatch(clt, e):
    try:
        e.parse()
        f = Cmd.get(e.cmd)
        if f:
            f(e)
            e.show()
    except (Restart, Stop):
        pass
    except Exception as ex:
        e.errors.append(ex)
        Cmd.events.append(e)
    finally:
        e.ready()
