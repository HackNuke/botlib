import sys

def getmain(name):
    return getattr(sys.modules["__main__"], name, None)


def kerror(txt):
    k = getmain("k")
    k.error(txt)


def klog(txt):
    k = getmain("k")
    k.log(txt)
