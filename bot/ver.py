# This file is in the Public Domain.

__version__ = 130

import time

starttime = time.time()

def ver(event):
    event.reply("BOT %s" % __version__)
