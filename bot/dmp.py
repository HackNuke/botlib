# This file is placed in the Public Domain.

from bot.obj import Object
from bot.tbl import Table

tbl = Table()

tbl.modnames = Object({'cmd': 'bot.adm', 'flt': 'bot.adm', 'thr': 'bot.adm', 'upt': 'bot.adm', 'fnd': 'bot.fnd', 'hlp': 'bot.hlp', 'cfg': 'bot.irc', 'dlt': 'bot.irc', 'met': 'bot.irc', 'mre': 'bot.irc', 'nck': 'bot.irc', 'ops': 'bot.irc', 'log': 'bot.log', 'pwd': 'bot.pwd', 'dpl': 'bot.rss', 'ftc': 'bot.rss', 'rem': 'bot.rss', 'rss': 'bot.rss', 'ver': 'bot.ver'})

tbl.names = Object({'bus': ['bot.bus.Bus'], 'object': ['bot.obj.Object'], 'command': ['bot.evt.Command'], 'enobot': ['bot.evt.ENoBot'], 'error': ['bot.evt.Error', 'bot.hdl.Error'], 'event': ['bot.evt.Event', 'bot.irc.Event'], 'output': ['bot.opt.Output'], 'break': ['bot.hdl.Break'], 'dispatcher': ['bot.hdl.Dispatcher'], 'enotimplemented': ['bot.hdl.ENotImplemented'], 'handler': ['bot.hdl.Handler'], 'loop': ['bot.hdl.Loop'], 'restart': ['bot.hdl.Restart'], 'stop': ['bot.hdl.Stop'], 'cfg': ['bot.irc.Cfg', 'bot.rss.Cfg', 'bot.run.Cfg', 'bot.udp.Cfg'], 'dcc': ['bot.irc.DCC'], 'irc': ['bot.irc.IRC'], 'user': ['bot.irc.User'], 'users': ['bot.irc.Users'], 'log': ['bot.log.Log'], 'db': ['bot.obj.Db'], 'default': ['bot.obj.Default'], 'enofile': ['bot.obj.ENoFile'], 'enojson': ['bot.obj.ENoJSON'], 'enomodule': ['bot.obj.ENoModule'], 'enotype': ['bot.obj.ENoType'], 'list': ['bot.obj.List'], 'enotxt': ['bot.prs.ENoTxt'], 'getter': ['bot.prs.Getter'], 'option': ['bot.prs.Option'], 'setter': ['bot.prs.Setter'], 'skip': ['bot.prs.Skip'], 'token': ['bot.prs.Token'], 'url': ['bot.prs.Url'], 'word': ['bot.prs.Word'], 'feed': ['bot.rss.Feed'], 'fetcher': ['bot.rss.Fetcher'], 'rss': ['bot.rss.Rss'], 'seen': ['bot.rss.Seen'], 'client': ['bot.run.Client'], 'runtime': ['bot.run.Runtime'], 'table': ['bot.tbl.Table'], 'thr': ['bot.thr.Thr'], 'repeater': ['bot.tms.Repeater'], 'timer': ['bot.tms.Timer'], 'udp': ['bot.udp.UDP']})
