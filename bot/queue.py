# This file is placed in the Public Domain.


"queued mixin"


import queue


from .object import Object


def __dir__():
    return (
        "Queued",
    )


class Queued(Object):


    def __init__(self):
        Object.__init__(self)
        self.queue = queue.Queue()

    def put(self, e):
        self.queue.put_nowait(e)
