# This file is placed in the Public Domain.


import inspect


import obot.bsc
import obot.irc
import obot.rss
import obot.udp


from otb import Cls, Cmd


def scan(mod):
    for k, o in inspect.getmembers(mod, inspect.isfunction):
         if "event" in o.__code__.co_varnames:
             Cmd.cmds[k] = o
    for k, clz in inspect.getmembers(mod, inspect.isclass):
       Cls.add(clz)


scan(obot.bsc)
scan(obot.irc)
scan(obot.rss)
scan(obot.udp)
