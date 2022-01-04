# This file is placed in the Public Domain.


import inspect
import os
import sys
import unittest


sys.path.insert(0, os.getcwd())


from ob.tbl import Tbl


from ob import Object, keys, values


import bot.bsc


Tbl.add(bot.bsc)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("bot.bsc" in keys(Tbl.mod))
