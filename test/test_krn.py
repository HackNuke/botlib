# This file is placed in the Public Domain.


import unittest


from bot.krn import getmain
from bot.ofn import dumps
from bot.run import Cfg


class Test_Kernel(unittest.TestCase):

    def test_cfg(self):
        k = getmain("k")
        self.assertEqual(type(k.cfg), Cfg)
