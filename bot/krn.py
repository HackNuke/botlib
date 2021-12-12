# This file is placed in the Public Domain.

import sys


def __dir__():
    return ("getmain", "kerror", "klog")


def getmain(name):
    m = getattr(sys.modules["__main__"], name, None)
    if not m:
        import bot.spc
        m = getattr(bot.spc, name, None)
    return m


def kerror(txt):
    k = getmain("k")
    k.error(txt)


def klog(txt):
    k = getmain("k")
    k.log(txt)
