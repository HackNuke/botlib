# This file is placed in the Public Domain.


"bot package modules"


from bot.tbl import Tbl


from bot import bus
from bot import cfg
from bot import clt
from bot import dbs
from bot import evt
from bot import fnc
from bot import jsn
from bot import krn
from bot import opt
from bot import prs
from bot import tbl
from bot import thr
from bot import tms


Tbl.add(bus)
Tbl.add(cfg)
Tbl.add(clt)
Tbl.add(dbs)
Tbl.add(evt)
Tbl.add(fnc)
Tbl.add(jsn)
Tbl.add(krn)
Tbl.add(opt)
Tbl.add(prs)
Tbl.add(tbl)
Tbl.add(thr)
Tbl.add(tms)


from bot import bsc
from bot import dbg
from bot import irc
from bot import opt
from bot import rss
from bot import tdr
from bot import udp
from bot import usr


Tbl.add(bsc)
Tbl.add(dbg)
Tbl.add(irc)
Tbl.add(opt)
Tbl.add(rss)
Tbl.add(tdr)
Tbl.add(udp)
Tbl.add(usr)
