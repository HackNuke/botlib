# This file is placed in the Public Domain.


import unittest


from obj import Object, get
from ocf import Cfg
from oev import Event
from ofn import fmt, idx
from ohd import Handler
from otb import Cmd, Obj


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
         idx(results, txt)
        
         
c = CLI()
results = Object()

import bot.all


class Test_Commands(unittest.TestCase):

    def test_commands(self):
        cmds = list(Cmd.cmds)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = Event(cmd + " " + ex, repr(c))
                c.handle(e)
                Obj.add(c)
                events.append(e)
        if Cfg.verbose:
            print(fmt(results, newline=True))
        