# This file is placed in the Public Domain.


"OTP-CR-117/19"


from bot.tbl import Tbl


from bot.mod import bsc
from bot.mod import dbg
from bot.mod import irc
from bot.mod import req
from bot.mod import rss
from bot.mod import udp
from bot.mod import wsd


Tbl.add(bsc)
Tbl.add(dbg)
Tbl.add(irc)
Tbl.add(req)
Tbl.add(rss)
Tbl.add(udp)
Tbl.add(wsd)
