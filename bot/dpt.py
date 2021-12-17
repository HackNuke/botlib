# This file is placed in the Public Domain.


from .obj import Object


def __dir__():
    return ("Dispatcher",)


class Dispatcher(Object):

    cbs = Object()

    @staticmethod
    def dispatch(event):
        if event and event.type in Dispatcher.cbs:
            Dispatcher.cbs[event.type](event)
        else:
            event.ready()

    @staticmethod
    def register(k, v):
        Dispatcher.cbs[str(k)] = v
