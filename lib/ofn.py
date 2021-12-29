# This file is placed in the Public Domain.


"object function"


import os
import pathlib


from obj import Object, items, keys


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


def edit(o, setter, skip=True, skiplist=None):
    if skiplist is None:
        skiplist = []
    count = 0
    for key, v in items(setter):
        if skip and v == "":
            del o[key]
        if key in skiplist:
            continue
        count += 1
        if v in ["True", "true"]:
            o[key] = True
        elif v in ["False", "false"]:
            o[key] = False
        else:
            o[key] = v
    return count


def fmt(o, keyz=None, empty=True, skip=None, newline=False):
    if keyz is None:
        keyz = keys(o) or ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in keyz:
        if key in skip:
            continue
        if key in dir(o):
            if key.startswith("__"):
                continue
            val = getattr(o, key, None)
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        if newline:
            result.append("%s=%s%s" % (k, v, "\n"))
        else:
            result.append("%s=%s%s" % (k, v, " "))
    if newline:
        txt += "\n".join([x.strip() for x in result])
    else:
        txt += " ".join([x.strip() for x in result])
    return txt


def idx(o, txt):
    o[str(o.__idx__)] = txt
    o.__idx__ += 1


def register(o, k, v):
    o.__dict__[str(k)] = v


def search(o, s):
    ok = False
    for k, v in items(s):
        vv = getattr(o, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok


def set(o, key, value):
    o.__dict__[key] = value


def spl(txt):
    return [x for x in txt.split(",") if x]
