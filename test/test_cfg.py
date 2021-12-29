# This file is placed in the Public Domain.


import unittest


from ocf import Cfg
from obj import Object, update
from ofn import edit
from opr import Parsed


class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        p = Parsed("m=irc")
        self.assertEqual(p.sets().m, "irc")

    def test_parse2(self):
        p = Parsed("m=irc,rss")
        self.assertEqual(p.sets().m, "irc,rss")

    def test_edit(self):
        d = Object({"mod": "irc,rss"})
        edit(Cfg, d)
        self.assertEqual(Cfg.mod, "irc,rss")
