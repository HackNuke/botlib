# This file is placed in the Public Domain.


"JSON tests"


import unittest


from bot.json import dumps, loads
from bot.object import Object


validjson = '{"test": "bla"}'


class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = Object()
        o.test = "bla"
        a = loads(dumps(o))
        self.assertEqual(a.test, "bla")

    def test_jsondump(self):
        o = Object()
        o.test = "bla"
        self.assertEqual(dumps(o), validjson)
