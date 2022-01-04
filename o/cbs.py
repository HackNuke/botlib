# This file is placed in the Public Domain.


from . import Object, get


class Cbs(Object):

    cbs = Object()

    @staticmethod
    def add(k, v):
        Cbs.cbs[str(k)] = v

    @staticmethod
    def get(typ):
        return get(Cbs.cbs, typ)

    @staticmethod
    def dispatch(event):
        if event and event.type in Cbs.cbs:
            Cbs.cbs[event.type](event)
