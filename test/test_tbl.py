# This file is placed in the Public Domain.


import inspect
import sys
import unittest


from ob.obj import Object, keys, values
from ob.tbl import Tbl

import mod.bsc


Tbl.add(mod.bsc)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("mod.bsc" in keys(Tbl.mod))
