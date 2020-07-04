# BOTLIB - the bot library !
#
#

import atexit, readline, sys, termios, threading

from .obj import Cfg, Object
from .hdl import Event
from .krn import k
from .prs import parse_cli
from .thr import launch

def __init__():
    return ("Cfg", "Console", "init")

resume = {}

def init(kernel):
    c = Console()
    c.start()
    return c

class Cfg(Cfg):

    pass

class Console(Object):

    def __init__(self):
        super().__init__(self)
        self.ready = threading.Event()

    def announce(self, txt):
        pass

    def input(self):
        while 1:
            event = self.poll()
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()
        self.ready.set()

    def poll(self):
        e = Event()
        e.speed = "fast"
        e.txt = input("> ")
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        setcompleter(k.cmds)
        launch(self.input)

    def wait(self):
        self.ready.wait()

def close_history():
    global HISTFILE
    if bot.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bot.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            cdir(HISTFILE)
            touch(HISTFILE)
        readline.write_history_file(HISTFILE)

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def enable_history():
    assert bot.obj.workdir
    global HISTFILE
    HISTFILE = os.path.abspath(os.path.join(bot.obj.workdir, "history"))
    if not os.path.exists(HISTFILE):
        cdir(HISTFILE)
        touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

def setcompleter(commands):
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def setup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def writepid():
    assert bot.obj.workdir
    path = os.path.join(bot.obj.workdir, "pid")
    if not os.path.exists(path):
        cdir(path)
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
