# This file is placed in the Public Domain.


from ob.tbl import Tbl


from bot import bsc
from bot import irc
from bot import rss
from bot import udp


Tbl.add(bsc)
Tbl.add(irc)
Tbl.add(rss)
Tbl.add(udp)
