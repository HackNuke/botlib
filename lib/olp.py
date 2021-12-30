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
        self.stopped = False

    def handle(self, e):
        pass

    def loop(self):
        while not self.stopped:
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, e):
        self.queue.put_nowait(e)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped = True
        self.queue.put(None)


    def wait(self):
        while 1:
            time.sleep(1.0)
    