# This file is placed in the Public Domain.


from o.tbl import Tbl

from bot import bsc
from bot import irc
from bot import log
from bot import rss
from bot import udp

Tbl.add(bsc)
Tbl.add(irc)
Tbl.add(log)
Tbl.add(rss)
Tbl.add(udp)
