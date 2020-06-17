# BOTLIB - the bot library !
#
# 

import os, queue, socket, ssl, sys, textwrap, time, threading, _thread

from .obj import Cfg, Object, locked
from .krn import k
from .thr import launch
from .hdl import Event, Handler
from .utl import get_exception

saylock = _thread.allocate_lock()

def init(k):
    i = IRC()
    i.start()
    return i

class Cfg(Cfg):

    pass

class Event(Event):

    def show(self, bot=None):
        for txt in self.result:
            k.fleet.say(self.orig, self.channel, txt)

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 480

class IRC(Handler):

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._trc = ""
        self.cc = "!"
        self.cfg = Cfg()
        self.cfg.update(k.cfg)
        self.channels = []
        self.state = Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        k.fleet.add(self)

    def _connect(self, server):
        try:
            oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        oldsock.setblocking(1)
        oldsock.settimeout(5.0)
        try:
            oldsock.connect((server, 6667))
        except (OSError, ConnectionError):
            time.sleep(2.0)
            try:
                oldsock.connect((server, 6667))
            except (OSError, ConnectionError):
                self._connected.set()
                return False
        oldsock.setblocking(1)
        oldsock.settimeout(700.0)
        self._sock = oldsock
        self._fsock = self._sock.makefile("r")
        fileno = self._sock.fileno()
        os.set_inheritable(fileno, os.O_RDWR)
        self._connected.set()
        return True

    def _parsing(self, txt):
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.orig = repr(self)
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
                o.etype = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    @locked(saylock)
    def _say(self, channel, txt, mtype="chat"):
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def _some(self, use_ssl=False, encoding="utf-8"):
        if use_ssl:
            inbytes = self._sock.read()
        else:
            inbytes = self._sock.recv(512)
        txt = str(inbytes, encoding)
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)
            
    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self, server, nick):
        nr = 0
        while 1:
            self.state.nrconnect += 1
            if self._connect(server):
                break
            time.sleep(10.0)
            nr += 1
        self._connected.wait()
        self.logon(server, nick)

    def dispatch(self, event):
        func = self.get_cmd(event.command)
        if func:
            func(event)

    def poll(self):
        self._connected.wait()
        if not self._buffer:
            try:
                self._some()
            except (OSError, ConnectionError) as ex:
                e = Event()
                e.type = "error"
                e.error = str(ex)
                e.trc = get_exception()
                return e
        e = self._parsing(self._buffer.pop(0))
        cmd = e.command
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "bot")
        return e

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        self._connected.wait()
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username or "okbot", server, server, self.cfg.realname or "okbot"))

    def input(self):
        while 1:
            e = self.poll()
            if not e:
                break
            self.put(e)

    def output(self):
        self._outputed = True
        while 1:
            channel, txt, type = self._outqueue.get()
            if channel == None:
                break
            if txt:
                time.sleep(0.001)
                self._say(channel, txt, type)

    def raw(self, txt):
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        try:
            self._sock.send(txt)
        except (OSError, ConnectionError) as ex:
            e = Event()
            e.error = str(ex) 
            e.trc = get_exception()
            self.put(e)
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt, mtype="chat"):
        self._outqueue.put_nowait((channel, txt, mtype))

    def start(self, cfg=None):
        if cfg:
            self.cfg.update(cfg)
        else:
            self.cfg.last()
        self.channels.append(self.cfg.channel or "#okbot")
        launch(self.doconnect)
        
    def doconnect(self):
        self.connect(self.cfg.server or "localhost", self.cfg.nick or "okbot")
        super().start()
        launch(self.input)
        launch(self.output)

    def stop(self):
        super().stop()
        self._outqueue.put((None, None, None))
        try:
            self._sock.shutdown(2)
        except OSError:
            pass

    def ERROR(self, event):
        self.state.nrerror += 1
        self.state.error = event.error
        self._connected.clear()
        self.stop()
        if self.state.nrerror < 3:
            init(k)

    def NOTICE(self, event):
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % (cfg.name or "OKBOT", "1", "the ok bot !")
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, event):
        if event.txt.startswith("DCC CHAT"):
            if k.cfg.users and not k.users.allowed(event.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.encoding = "utf-8"
                launch(dcc.connect, event)
                return
            except ConnectionError:
                return
        if event.txt and event.txt[0] == handler.cc:
            if k.cfg.users and not k.users.allowed(event.origin, "USER"):
               return
            e = Event(event.txt[1:])
            e.orig = event.orig
            e.origin = event.origin
            k.put(e)

    def QUIT(self, event):
        if self.cfg.server in event.orig:
            self.stop()
        
class DCC(Handler):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""
        k.fleet.add(self)
        
    def raw(self, txt):
        self._fsock.write(str(txt).rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        self.raw(txt)

    def connect(self, event):
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((addr, port))
        except ConnectionError:
            return
        s.send(bytes('Welcome to %s %s !!\n' % (k.cfg.name, event.nick), "utf-8"))
        s.setblocking(1)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.origin = event.origin
        self.launch(self.input)
        super().start()
        self._connected.set()

    def input(self):
        while 1:
            try:
                e = self.poll()
            except EOFError:
                break
            k.put(e)

    def poll(self):
        self._connected.wait()
        e = Event()
        e.txt = self._fsock.readline()
        e.txt = e.txt.rstrip()
        try:
            e.args = e.txt.split()[1:]
        except ValueError:
            e.args = []
        e._sock = self._sock
        e._fsock = self._fsock
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        e.parse()
        return e

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
