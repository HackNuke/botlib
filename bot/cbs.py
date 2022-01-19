# This file is placed in the Public Domain.


"table"


import _thread


from .cmd import Cmd
from .err import Restart, Stop
from .fnc import register
from .obj import Object, get


def __dir__():
    return (
        "Cbs",
    )


class Cbs(Object):

    cbs = Object()
    events = []

    @staticmethod
    def add(name, cb):
        register(Cbs.cbs, name, cb)

    @staticmethod
    def callback(clt, e):
        try:
            f = Cbs.get(e.type)
            if f:
                f(clt, e)
            else:
                e.ready()
        except (Restart, Stop):
            pass
        except Exception as ex:
            e.errors.append(ex)
            Cbs.events.append(e)
        finally:
            e.ready()

    @staticmethod
    def get(cmd):
        return get(Cbs.cbs, cmd)
