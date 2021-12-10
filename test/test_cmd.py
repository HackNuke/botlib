# This file is placed in the Public Domain.


import unittest


from bot.krn import getmain
from bot.obj import Object, get, indexed
from bot.tbl import Table


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

class Test_Commands(unittest.TestCase):

    def test_commands(self):
        k = getmain("k")
        c = k.first()
        cmds = list(Table.modnames)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = c.event(cmd + " " + ex)
                k.dispatch(e)
                cmdstr = cmd + " " + ex
                events.append(e)
