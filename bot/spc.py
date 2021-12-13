# This file is placed in the Public Domain.


from bot.run import Runtime


k = Runtime()


def kernel():
    global k
    if k:
        return k
    k = getmain("k")
   