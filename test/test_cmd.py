# This file is placed in the Public Domain.


import unittest


from ol.cls import Cls
from ol.cmd import Cmd
from ol.cfg import Cfg
from ol.obj import Object, get
from ol.evt import Event
from ol.fnc import format, index
from ol.hdl import Handler


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


class Test_Commands(unittest.TestCase):

    def test_commands(self):
        cmds = list(Cmd.cmds)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                c.handle(e)
                events.append(e)
        if Cfg.verbose:
            print(format(results, newline=True))
        