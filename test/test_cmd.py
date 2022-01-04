# This file is placed in the Public Domain.


import inspect
import unittest


from ob.cls import Cls
from ob.cmd import Cmd
from ob.cfg import Cfg
from ob.obj import Object, get, values
from ob.evt import Event
from ob.fnc import format, index
from ob.hdl import Handler
from ob.tbl import Tbl


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


class CLI(Handler):


     def raw(self, txt):
         index(results, txt)
        
         
c = CLI()
results = Object()


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


def scan():
    for mod in values(Tbl.mod):
        for k, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                Cmd.cmds[k] = o
        for k, clz in inspect.getmembers(mod, inspect.isclass):
            Cls.add(clz)
        Tbl.add(mod)


import tob.all


class Test_Commands(unittest.TestCase):

    def test_commands(self):
        scan()
        cmds = list(Cmd.cmds)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                c.handle(e)
                events.append(e)
        consume(events)
        self.assertTrue(not events)
