# This file is placed in the Public Domain.


import html.parser
import re
import threading
import urllib


from obj import Object, get, update
from ocf import Cfg
from odb import Db, find, last, save
from odf import Default
from ofn import edit
from otb import Obj 
from otm import Repeater
from oth import launch


from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen


def __dir__():
    return (
        "Cfg",
        "Feed",
        "Rss",
        "Seen",
        "Fetcher",
        "dpl",
        "ftc",
        "rem",
        "rss"
    )


class Feed(Object):

    def __getattr__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            self[key] = ""
            return self[key]


class Rss(Object):

    def __init__(self):
        super().__init__()
        self.rss = ""


class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []


class Fetcher(Object):

    seen = Seen()

    def __init__(self):
        super().__init__()
        self.connected = threading.Event()

    def display(self, o):
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = "title,link"
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = get(o, key, None)
            if not data:
                continue
            data = data.replace("\n", " ")
            data = striphtml(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, feed):
        counter = 0
        objs = []
        for o in reversed(list(getfeed(feed.rss))):
            f = Feed()
            update(f, dict(o))
            update(f, feed)
            if "link" in f:
                u = urllib.parse.urlparse(f.link)
                if u.path and not u.path == "/":
                    url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
                else:
                    url = f.link
                if url in Fetcher.seen.urls:
                    continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
        if objs:
            save(Fetcher.seen)
        for o in objs:
            txt = self.display(o)
            Obj.announce(txt)
        return counter

    def run(self):
        thrs = []
        for _fn, o in find("rss"):
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()


def getfeed(url):
    if Cfg.debug:
        return [Object(), Object()]
    try:
        result = geturl(url)
    except (ValueError, HTTPError, URLError):
        return [Object(), Object()]
    if not result:
        return [Object(), Object()]
    import feedparser
    result = feedparser.parse(result.data)
    if result and "entries" in result:
        for entry in result["entries"]:
            yield entry


def gettinyurl(url):
    postarray = [
        ("submit", "submit"),
        ("url", url),
    ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request("http://tinyurl.com/create.php",
                  data=bytes(postdata, "UTF-8"))
    req.add_header("User-agent", useragent(url))
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()
    return []


def geturl(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header("User-agent", useragent("BOTLIB"))
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response


def striphtml(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def unescape(text):
    txt = re.sub(r"\s+", " ", text)
    return html.unescape(txt)


def useragent(txt):
    return "Mozilla/5.0 (X11; Linux x86_64) " + txt


def dpl(event):
    if len(event.args) < 2:
        event.reply("dpl <stringinurl> <item1,item2>")
        return
    db = Db()
    setter = {"display_list": event.args[1]}
    name = get(db.names, "rss", "rss")
    _fn, o = db.lastmatch(name, {"rss": event.args[0]})
    if o:
        edit(o, setter)
        save(o)
        event.reply("ok")


def ftc(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply(",".join([str(x) for x in res]))
        return


def rem(event):
    if not event.args:
        event.reply("rem <stringinurl>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for _fn, o in find("rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")


def rss(event):
    if not event.args:
        event.reply("rss <url>")
        return
    url = event.args[0]
    if "http" not in url:
        event.reply("i need an url")
        return
    res = list(find("rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    save(o)
    event.reply("ok")
