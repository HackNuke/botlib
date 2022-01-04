# This file is placed in the Public Domain.


import inspect
import unittest


from ob.bus import Bus
from ob.cls import Cls
from ob.clt import Client
from ob.cmd import Cmd
from ob.evt import Event
from ob.fnc import format
from ob.hdl import Handler
from ob.krn import Cfg
from ob.tbl import Tbl


from ob import Object, get, values


events = []


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["nick=botje", "server=localhost", ""]
param.dlt = ["root@shell"]
param.dne = ["test4", ""]
param.dpl = ["reddit title,summary,link"]
param.flt = ["0", ""]
param.fnd = ["cfg", "log", "rss", "cfg server==localhost", "rss rss==reddit"]
param.log = ["test1", ""]
param.met = ["root@shell"]
param.nck = ["botje"]
param.pwd = ["bart blabla"]
param.rem = ["reddit", ""]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["things todo"]


class CLI(Handler, Client):


     def __init__(self):
         Client.__init__(self)
         Handler.__init__(self)

     def raw(self, txt):
         results.append(txt)
         if Cfg.verbose:
             print(txt)
        
         
c = CLI()
results = []


def consume(events):
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


class Test_Commands(unittest.TestCase):

    def setUp(self):
        c.start()
        
    def tearDown(self):
        c.stop()

    def test_commands(self):
        cmds = sorted(Cmd.cmds)
        for cmd in cmds:
            for ex in getattr(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                c.handle(e)
                events.append(e)
        consume(events)
        self.assertTrue(not events)
