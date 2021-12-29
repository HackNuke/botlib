# This file is placed in the Public Domain.


import sys
import unittest


sys.path.insert(0, "lib")


from obj import Object, keys
from otb import Tbl


import bot.all


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("bot.bsc" in keys(Tbl.mod))
