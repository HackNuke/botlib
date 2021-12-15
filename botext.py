# This file is placed in the Public Domain


import os
import sys
import termios
import traceback


def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if elem[0].endswith(".py"):
            plugfile = elem[0][:-3].split(os.sep)
        else:
            plugfile = elem[0].split(os.sep)
        mod = []
        for element in plugfile[:-2:-1]:
            mod.append(element.split(".")[-1])
        ownname = ".".join(mod[::-1])
        result.append("%s:%s" % (ownname, elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res


def privileges(self, name, group):
    if not self.root():
        self.log("you need root privileges to run botc")
        return False
    try:
        pwn = pwd.getpwnam(name)
    except (TypeError, KeyError):
        self.log('add group/user with 1) groupadd botd 2) useradd -b /var/lib -d /var/lib/botd -m -g botd botd')
        return False
    try:
        pwn = pwd.getpwnam(name)
    except (TypeError, KeyError):
        return False
    if not os.path.exists(ObjCfg.wd):
        os.mkdir(ObjCfg.wd)
    cdir(ObjCfg.wd + os.sep)
    os.chown(ObjCfg.wd, pwn.pw_uid, pwn.pw_gid)
    cdir(os.path.join(ObjCfg.wd, "store", ""))
    os.chown(os.path.join(ObjCfg.wd, "store", ""), pwn.pw_uid, pwn.pw_gid)
    os.setgroups([])
    os.setgid(pwn.pw_gid)
    os.setuid(pwn.pw_uid)
    os.umask(Cfg.mask)
    self.cfg.uuids = os.getresuid()
    return True


def root():
    if os.geteuid() != 0:
        return False
    return True


def wrap(func):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
