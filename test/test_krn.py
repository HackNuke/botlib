# This file is placed in the Public Domain.


import unittest


from bot.krn import kernel
from bot.run import Cfg as RunCfg


class Test_Kernel(unittest.TestCase):

    def test_cfg(self):
        k = kernel()
        self.assertEqual(type(k.cfg), RunCfg)
