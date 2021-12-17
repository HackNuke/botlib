# This file is placed in the Public Domain.


import os
import pathlib
import shutil
import sys
import termios


def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def skel(wd): 
    if os.path.exists(wd):
        shutil.rmtree(wd)
        os.sync()
    else:
        cdir(wd)


def wrap(func):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
