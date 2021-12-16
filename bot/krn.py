# This file is placed in the Public Domain.


from bot.run import Runtime
from bot.tbl import Table

class Kernel(Runtime):

    def init(self, mns, pn, threaded=False):
        Table.init(mns, pn, threaded)
        
    def scan(self, skip=None):
        Table.scan(skip)

k = Kernel()
