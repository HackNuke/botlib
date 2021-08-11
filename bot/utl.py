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


def fmt(o, keys=None, empty=True, skip=None):
    if keys is None:
        keys = o.keys()
    if not keys:
        keys = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in sorted(keys):
        if key in skip:
            continue
        if key in o:
            val = o[key]
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()


def fns(name, timed=None):
    if not name:
        return []
    p = os.path.join(wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(p) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)


def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t


def getname(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__


def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    mn, cn = cname.rsplit(".", 1)
    mod = sys.modules.get(mn, None)
    if not mod:
        raise NoModule(mn)
    t = getattr(mod, cn, None)
    if fn:
        o = t()
        o.load(fn)
        return o
    raise NoType(cname)


def launch(func, *args, **kwargs):
    name = kwargs.get("name", getname(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t


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
