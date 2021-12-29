# This file is placed in the Public Domain.


import unittest


from obj import Object
from odb import Db
from ojs import dumps, loads


class Composite(Object):

    def __init__(self):
        super().__init__()
        self.db = Db()



class Test_Composite(unittest.TestCase):

    def test_composite(self):
        c = Composite()
        s = dumps(c)
        a = loads(dumps(c))
        self.assertEqual(type(a.db), Object)
