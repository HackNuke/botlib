# BOTLIB - the bot library !
#
#

import importlib, queue

from .itr import find_cmds
from .prs import Parsed
from .obj import Object
from .tbl import names
from .thr import launch

def direct(name):
    return importlib.import_module(name)

class NOTIMPLEMENTED(Exception):

    pass

class ETYPE(Exception):

    pass

class Event(Parsed):

    pass

        
class Handler(Object):
 
    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.queue = queue.Queue()
        self.table = Object()
                
    def dispatch(self, event):
        if not event.cmd and event.txt:
            event.cmd = event.txt.split()[0]
        event.func = self.get_cmd(event.cmd)
        if event.func:
            event.func(event)
            event.show()
            
    def get_cmd(self, cmd, dft=None):
        func = self.cmds.get(cmd, None)
        print(func)
        if not func:
            name = names.get(cmd, None)
            if name:
                print("autoload %s" % name) 
                self.load_mod(name)
                func = self.cmds.get(cmd, dft)
        return func

    def handler(self):
        while 1:
            event = self.queue.get()
            if event is None:
                break
            print(event)
            launch(self.dispatch, event)

    def load_mod(self, name):
        self.table[name] = mod = direct(name)
        self.cmds.update(find_cmds(mod))
        return self.table[name]

    def put(self, event):
        self.queue.put(event)

    def register(self, cmd, func):
        self.cmds[cmd] = func

    def scan(self, mod):
        self.cmds.update(find_cmds(mod))

    def start(self):
        launch(self.handler)
            
    def stop(self):
        self.queue.put(None)

