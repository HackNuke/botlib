# This file is placed in the Public Domain.


import unittest


from obj import Object
from ojs import dumps, loads

validjson = '{"test": "bla"}'
validjson = '{"test": "bla", "__otype__": "obj.Object"}'

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

