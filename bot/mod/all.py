# This file is placed in the Public Domain.

"bot.mod package modules"


from bot.tbl import Tbl


from bot.mod import bsc
from bot.mod import irc
from bot.mod import rss
from bot.mod import udp


Tbl.add(bsc)
Tbl.add(irc)
Tbl.add(rss)
Tbl.add(udp)
