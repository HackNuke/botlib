# This file is in the Public Domain.

__version__ = 10

import time

starttime = time.time()

def ver(event):
    event.reply("GCID %s" % __version__)
