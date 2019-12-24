# BOTLIB - Framework to program bots.
#
# shell related code.

import argparse
import atexit
import bl
import logging
import optparse
import os
import readline
import time

from bl import Cfg, cfg, default
from bl.log import level, logfiled
from bl.trm import reset, save
from bl.utl import cdir, hd, touch
from bl.trc import get_exception

cmds = []

HISTFILE = ""

def __dir__():
    return ("daemon", "execute", "parse_cli", "set_completer")

def close_history():
    global HISTFILE
    assert bl.workdir
    if not HISTFILE:
        HISTFILE = os.path.join(bl.workdir, "history")
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
    global HISTFILE
    assert bl.workdir
    HISTFILE = os.path.abspath(os.path.join(bl.workdir, "history"))
    if not os.path.exists(HISTFILE):
        touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    save()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except Exception:
        logging.error(get_exception())
    reset()
    close_history()

def get_completer():
    return readline.get_completer()

def make_opts(ns, options, **kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    for opt in options:
        if not opt:
            continue
        if opt[2] == "store":
            parser.add_argument(opt[0], opt[1], action=opt[2], type=opt[3], help=opt[4], dest=opt[5])
        else:
            parser.add_argument(opt[0], opt[1], action=opt[2], default=opt[3], help=opt[4], dest=opt[5])
    parser.add_argument('args', nargs='*')
    parser.parse_known_args(namespace=ns)
  
def parse_cli(name="botlib", version=None, opts=[], wd=None, loglevel="error"):
    cfg = Cfg(default)
    make_opts(cfg, opts)
    cfg.debug = False
    cfg.name = name
    cfg.version = version
    cfg.workdir = cfg.workdir or wd or hd(".%s" % cfg.name)
    cfg.logdir = cfg.logdir or os.path.join(cfg.workdir, "logs")
    cfg.txt = " ".join(cfg.args)
    sp = os.path.join(cfg.workdir, "store") + os.sep
    if not os.path.exists(sp):
        cdir(sp)
    bl.workdir = cfg.workdir
    level(cfg.level or loglevel, cfg.logdir)
    bl.update(bl.cfg, cfg)
    logging.warning("%s started (%s) at %s" % (cfg.name.upper(), cfg.level or loglevel, time.ctime(time.time())))
    logging.warning("logging at %s" % logfiled)
    return bl.cfg

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def writepid():
    path = os.path.join(cfg.workdir, "botlib.pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
