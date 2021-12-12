# This file is placed in the Public Domain.


import unittest


from bot.krn import getmain
from bot.obj import Cfg
from bot.ofn import dumps
from bot.run import Runtime
from bot.run import Cfg as RunCfg


class Test_Kernel(unittest.TestCase):

    def test_cfg(self):
        k = getmain("k")
        if not k:
            k = Runtime()
        self.assertEqual(type(k.cfg), RunCfg)
