# This file is placed in the Public Domain.

"parse"

from .obj import Default

class Token(Default):
    "basic token"
    pass


class Word(Token):
    "token with txt"
    def __init__(self, txt):
        super().__init__()
        self.txt = txt


class Option(Token):
    "token starting with '--' or '-'" 
    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        if txt.startswith("-"):
            self.opt = txt[1:]


class Getter(Token):
    "matching key==value."
    def __init__(self, txt):
        super().__init__()
        if "==" in txt:
            pre, post = txt.split("==", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Setter(Token):
    "key=value combination."
    def __init__(self, txt):
        super().__init__()
        if "=" in txt:
            pre, post = txt.split("=", 1)
        else:
            pre = post = ""
        if pre:
            self[pre] = post


class Skip(Token):
    "token ending in '-'"
    def __init__(self, txt):
        super().__init__()
        pre = ""
        if txt.endswith("-"):
            if "=" in txt:
                pre, _post = txt.split("=", 1)
            elif "==" in txt:
                pre, _post = txt.split("==", 1)
            else:
                pre = txt
        if pre:
            self[pre] = True


class Url(Token):
    "url token."
    def __init__(self, txt):
        super().__init__()
        if txt.startswith("http"):
            self["url"] = txt


def parse_txt(o, ptxt=None):
    "parse text into an event."
    if ptxt is None:
        raise NoTextError(o)
    o.txt = ptxt
    o.otxt = ptxt
    o.gets = o.gets or Default()
    o.opts = o.opts or Default()
    o.timed = []
    o.index = None
    o.sets = o.sets or Default()
    o.skip = o.skip or Default()
    args = []
    for token in [Word(txt) for txt in ptxt.split()]:
        u = Url(token.txt)
        if u:
            args.append(u.url)
            continue
        s = Skip(token.txt)
        if s:
            o.skip.update(s)
            token.txt = token.txt[:-1]
        s = Setter(token.txt)
        if s:
            o.sets.update(s)
            continue
        g = Getter(token.txt)
        if g:
            o.gets.update(g)
            continue
        opt = Option(token.txt)
        if opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            if len(opt.opt) > 1:
                for op in opt.opt:
                    o.opts[op] = True
            else:
                o.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o


def parse_ymd(daystr):
    "parse ymd (year/month/day) string."
    valstr = ""
    val = 0
    total = 0
    for c in daystr:
        if c in "1234567890":
            vv = int(valstr)
        else:
            vv = 0
        if c == "y":
            val = vv * 3600 * 24 * 365
        if c == "w":
            val = vv * 3600 * 24 * 7
        elif c == "d":
            val = vv * 3600 * 24
        elif c == "h":
            val = vv * 3600
        elif c == "m":
            val = vv * 60
        else:
            valstr += c
        total += val
    return total
