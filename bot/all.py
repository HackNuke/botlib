# This file is placed in the Public Domain.


import inspect


import bot.bsc
import bot.irc
import bot.rss
import bot.udp


from otb import Cls, Cmd, Tbl


def scan(mod):
    for k, o in inspect.getmembers(mod, inspect.isfunction):
         if "event" in o.__code__.co_varnames:
             Cmd.cmds[k] = o
    for k, clz in inspect.getmembers(mod, inspect.isclass):
       Cls.add(clz)
    Tbl.add(mod)

scan(bot.bsc)
scan(bot.irc)
scan(bot.rss)
scan(bot.udp)
