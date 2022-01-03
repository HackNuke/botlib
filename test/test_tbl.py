# This file is placed in the Public Domain.


import inspect
import sys
import unittest


from ol.obj import Object, keys, values
from ol.tbl import Tbl


import bot.bsc


Tbl.add(bot.bsc)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("bot.bsc" in keys(Tbl.mod))
