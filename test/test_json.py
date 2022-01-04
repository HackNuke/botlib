# This file is placed in the Public Domain.


import unittest


from ob.jsn import dumps, loads

#validjson = '{"test": "bla", "otype": "Object"}'
validjson = '{"test": "bla"}'


from ob import Object

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

