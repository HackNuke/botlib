# This file is placed in the Public Domain.

import bot

tbl = bot.Default()

bot.update(tbl, {"modnames": {"cfg": "bot.cmd.cfg", "cmd": "bot.cmd.cmd", "dlt": "bot.usr", "flt": "bot.cmd.adm", "fnd": "bot.cmd.fnd", "krn": "bot.cmd.adm", "met": "bot.usr", "mod": "bot.cmd.adm", "thr": "bot.cmd.adm", "ver": "bot.ver"}, "names": {"bus": ["bot.bus.Bus"], "cfg": ["bot.Cfg", "bot.irc.Cfg"], "command": ["bot.evt.Command"], "console": ["bot.csl.Console"], "core": ["bot.hdl.Core"], "dcc": ["bot.irc.DCC"], "default": ["bot.Default"], "event": ["bot.evt.Event", "bot.irc.Event"], "getter": ["bot.prs.Getter"], "handler": ["bot.hdl.Handler"], "irc": ["bot.irc.IRC"], "object": ["bot.Object"], "objectlist": ["bot.ObjectList"], "option": ["bot.prs.Option"], "repeater": ["bot.clk.Repeater"], "select": ["bot.sel.Select"], "selectconsole": ["bot.csl.SelectConsole"], "setter": ["bot.prs.Setter"], "shell": ["bot.csl.Shell"], "skip": ["bot.prs.Skip"], "test": ["bot.csl.Test"], "timed": ["bot.prs.Timed"], "timer": ["bot.clk.Timer"], "token": ["bot.prs.Token"], "user": ["bot.usr.User"], "users": ["bot.usr.Users"]}, "pnames": {"adm": "bot.cmd.adm", "bus": "bot.bus", "cfg": "bot.cmd.cfg", "clk": "bot.clk", "cmd": "bot.cmd.cmd", "csl": "bot.csl", "dbs": "bot.dbs", "evt": "bot.evt", "fnd": "bot.cmd.fnd", "hdl": "bot.hdl", "irc": "bot.irc", "itr": "bot.itr", "krn": "bot.krn", "prs": "bot.prs", "sel": "bot.sel", "tbl": "bot.tbl", "thr": "bot.thr", "usr": "bot.usr", "utl": "bot.utl", "ver": "bot.ver"}})