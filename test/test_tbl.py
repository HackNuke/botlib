# This file is placed in the Public Domain.


import inspect
import sys
import unittest


sys.path.insert(0, "lib")


from obj import Object, keys
from otb import Cls, Cmd, Tbl


import bot.bsc


def scan(mod):
    Tbl.add(mod)
    for k, o in inspect.getmembers(mod, inspect.isfunction):
         if "event" in o.__code__.co_varnames:
             Cmd.cmds[k] = o
    for k, clz in inspect.getmembers(mod, inspect.isclass):
       Cls.add(clz)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        scan(bot.bsc)
        self.assertTrue("bot.bsc" in keys(Tbl.mod))
