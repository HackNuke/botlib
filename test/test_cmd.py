# This file is placed in the Public Domain.


import unittest


from bot.clt import Client
from bot.krn import getmain
from bot.obj import Cfg, Object, get, indexed
from bot.run import Runtime
from bot.tbl import Table


Cfg.wd = "reproduced"


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

class Kernel(Runtime):

    def error(self, txt):
        print(txt)
        sys.stdout.flush()

    def log(self, txt):
        if "PONG" in txt or "PING" in txt:
            return
        if self.cfg.verbose:
            print(txt.rstrip())
            sys.stdout.flush()

k = getmain("k")
if not k:
    k = Kernel()
results = Object()

class CLI(Client):

    def __init__(self):
        super().__init__()
        k.add(self)

    def raw(self, txt):
        global results
        indexed(results, txt)


c = CLI()
    

import bot.all


class Test_Commands(unittest.TestCase):

    def test_commands(self):
        cmds = list(Table.modnames)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = c.event(cmd + " " + ex)
                k.dispatch(e)
                cmdstr = cmd + " " + ex
                events.append(e)
