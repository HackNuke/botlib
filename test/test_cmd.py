# This file is placed in the Public Domain.

import unittest

from bot.bus import Bus
from bot.obj import Object
from bot.krn import kernel

events = []
k = kernel()

param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["cfg server=localhost", "cfg", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", ""]
param.fnd = [
    "bot.irc.Cfg",
    "bot.log.Log",
    "bot.tdo.Todo",
    "bot.rss.Rss",
    "bot.irc.Cfg server==localhost",
    "bot.rss.Rss rss==reddit rss",
]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]


class Test_Commands(unittest.TestCase):
    def test_commands(self):
        c = Bus.first()
        l = list(k.cmds)
        for cmd in l:
            for ex in getattr(param, cmd, [""]):
                e = c.event(cmd + " " + ex)
                k.dispatch(e)
                events.append(e)
