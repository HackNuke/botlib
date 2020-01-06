# BOTLIB - Framework to program bots (a botlib).
#
# fuzzer tests.

import logging
import random
import unittest

from bl.krn import Kernel
from bl.typ import get_cls
from bl.usr import Users

k = Kernel()
k.cfg.prompt = False
k.walk("bl")
k.start()

users = Users()
users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for t in k.names.values():
            for key in k.names:
                try:
                    e = get_cls(t)()
                    e.verbose = k.cfg.verbose
                    e.txt = key + " " + random.choice(k.names.values())
                    e.orig = repr(k)
                    e.origin = "test@shell"
                    v = k.get_cmd(key)
                    if v:
                        v(e)
                except AttributeError:
                    pass
                except TypeError as ex:
                    break
        self.assertTrue(True)