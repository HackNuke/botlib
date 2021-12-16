# This file is placed in the Public Domain.


import unittest


from bot.obj import Cfg, Object, values
from bot.ofn import dumps
from bot.tbl import Table

import bot.all

class Test_Table(unittest.TestCase):

    def test_tblclasses(self):
        Table.scan("bot", skip="bot.irc")
        self.assertTrue(Object in values(Table.classes))

