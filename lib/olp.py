# This file is placed in the Public Domain.


"object loop"


import queue
import time


from obj import Object
from oth import launch


class Loop(Object):

    def __init__(self):
        Object.__init__(self)
        self.queue = queue.Queue()

    def handle(self, e):
        pass

    def loop(self):
        while 1:
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, e):
        self.queue.put_nowait(e)

    def start(self):
        launch(self.loop)

    def wait(self):
        while 1:
            time.sleep(1.0)
    