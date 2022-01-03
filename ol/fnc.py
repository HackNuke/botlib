# This file is placed in the Public Domain.


"object utility"


import os
import pathlib


from .obj import Object, get, items, keys


def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def diff(o1, o2):
    d = Object()
    for k in keys(o2):
        if k in keys(o1) and o1[k] != o2[k]:
            d[k] = o2[k]
    return d


def edit(o, setter):
    for key, v in items(setter):
        register(o, key, v)


def format(o, skip="", *args, **kwargs):
    res = ""
    for k in keys(o):
        if k in spl(skip):
            continue
        v = get(o, k, None)
        print(v)
        res += "%s=%s " % (k, v)
    return res.rstrip()


def index(o, txt):
    o[str(o.__idx__)] = txt
    o.__idx__ += 1


def register(o, k, v):
    setattr(o, k, v)


def search(o, s):
    ok = False
    for k, v in items(s):
        vv = getattr(o, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok


def zet(o, key, value):
    o.__dict__[key] = value


def spl(txt):
    return [x for x in txt.split(",") if x]
