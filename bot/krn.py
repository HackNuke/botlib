# This file is placed in the Public Domain.

import sys

from bot.run import Runtime

k = None


def __dir__():
    return ("getmain", "k", "kerror", "klog")


def getmain(name):
    return getattr(sys.modules["__main__"], name, None)


def kernel():
    global k
    if k:
        return k
    k = getmain("k")
    if not k:
        k = Runtime()


def kerror(txt):
    k.error(txt)


def klog(txt):
    k.log(txt)

   