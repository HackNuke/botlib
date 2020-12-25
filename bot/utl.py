# BOTLIB - utl.py
#
# this file is placed in the public domain

"utilities file"

# imports

import datetime
import importlib
import os
import random
import re
import socket
import sys
import time
import traceback
import urllib


try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
    "%d, %b %Y %H:%M:%S +0000"
]

# functions

def cdir(path):
    "create directory"
    if os.path.exists(path):
        return
    res = ""
    path2, _fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
            os.chmod(padje, 0o700)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass

def day():
    "return this day"
    return str(datetime.datetime.today()).split()[0]

def direct(name, pname=''):
    "load a module"
    return importlib.import_module(name, pname)

def file_time(timestamp):
    s = str(datetime.datetime.fromtimestamp(timestamp))
    return s.replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def fntime(daystr):
    "return time from filename"
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    try:
        datestr, rest = datestr.rsplit(".", 1)
    except ValueError:
        rest = ""
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            t += float("." + rest)
    except ValueError:
        t = 0
    return t

def get_cls(name):
    "return class from full qualified name"
    try:
        modname, clsname = name.rsplit(".", 1)
    except Exception as ex:
        raise ENOCLASS(name) from ex
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_exception(txt="", sep=" "):
    "print exception trace"
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        res = []
        for x in elem[0].split(os.sep)[::-1]:
            if x in ["bot"]:
                break
            res.append(x)
        result.append("%s:%s" % (os.sep.join(res[::-1]), elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

def get_tinyurl(url):
    "return a corresponding timyurl"
    postarray = [
        ('submit', 'submit'),
        ('url', url),
        ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php', data=bytes(postdata, "UTF-8"))
    req.add_header('User-agent', useragent())
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()
    return []

def get_url(url):
    "return a http page"
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def locked(l):
    "lock descriptor"
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockeddec.__doc__ = func.__doc__
        return lockedfunc
    return lockeddec

def mods(mn, name="bot"):
    "return all modules in a package"
    mod = []
    pkg = direct(mn)
    path = pkg.__file__ or pkg.__path__[0]
    for m in ["%s.%s" % (name, x.split(os.sep)[-1][:-3]) for x in os.listdir(path)
              if x.endswith(".py")
              and not x == "setup.py"]:
        mod.append(direct(m))
    return mod

def spl(txt):
    "return comma splitted values"
    return iter([x for x in txt.split(",") if x])

def strip_html(text):
    "strip html codes from a page"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def to_time(daystr):
    "convert a timestring to unix timestamp"
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
            break
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    return res

def toudp(host, port, txt):
    "send text over udp to the udp to irc relay server"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))

def unescape(text):
    "unescape html codes"
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    "return useragent"
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTLIB +http://pypi.org/project/botlib)'
