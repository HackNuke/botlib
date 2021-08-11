# This file is placed in the Public Domain.

"utilities"

def day():
    return str(datetime.datetime.today()).split()[0]


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365 * 24 * 60 * 60
    week = 7 * 24 * 60 * 60
    nday = 24 * 60 * 60
    hour = 60 * 60
    minute = 60
    years = int(nsec / year)
    nsec -= years * year
    weeks = int(nsec / week)
    nsec -= weeks * week
    nrdays = int(nsec / nday)
    nsec -= nrdays * nday
    hours = int(nsec / hour)
    nsec -= hours * hour
    minutes = int(nsec / minute)
    sec = nsec - minutes * minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt

def spl(txt):
    return [x for x in txt.split(",") if x]


def listfiles(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def parse_txt(o, ptxt=None):
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

def run(txt, p):
    class Out(Client):
        def raw(self, txt):
            p(txt)
    c = Out()
    res = c.cmd(txt)
    return res
