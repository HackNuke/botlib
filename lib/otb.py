# This file is placed in the Public Domain.


"object table"


from obj import Object, get, items, values
from ofn import idx, register


class NoObj(Exception):

    pass


class Cbs(Object):

    cbs = Object()

    @staticmethod
    def add(k, v):
        Cbs.cbs[str(k)] = v

    @staticmethod
    def get(typ):
        return get(Cbs.cbs, typ)

    @staticmethod
    def dispatch(event):
        if event and event.type in Cbs.cbs:
            Cbs.cbs[event.type](event)


class Cls(Object):

    cls = Object()

    @staticmethod
    def add(clz):
        register(Cls.cls, "%s.%s" % (clz.__module__, clz.__name__), clz)

    @staticmethod
    def full(name):
        name = name.lower()
        res = []
        for cln in Cls.cls:
            if cln.split(".")[-1].lower() == name:
                res.append(cln)
        return res

    @staticmethod
    def get(nm):
        return get(Cls.cls, nm)

class Cmd(Object):

    cmds = Object()

    @staticmethod
    def add(cmd):
        register(Cmd.cmds, cmd.__name__, cmd)

    @staticmethod
    def dispatch(e):
        f = Cmd.get(e.cmd)
        if f:
            f(e)
            e.show()

    @staticmethod
    def get(cmd):
        return get(Cmd.cmds, cmd)


class Tbl(Object):

    mod = Object()

    @staticmethod
    def add(o):
        Tbl.mod[o.__name__] = o

    @staticmethod
    def get(nm):
        return get(Tbl.mod, nm, None)


class Obj(Object):

    objs = Object()

    @staticmethod
    def add(o):
        if o not in values(Obj.objs):
            idx(Obj.objs, o)

    @staticmethod
    def announce(txt):
        for o in values(Obj.objs):
            o.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in values(Obj.objs):
            if repr(o) == orig:
                return o
        raise NoObj(orig)
        
    @staticmethod
    def say(orig, channel, txt):
        o = Obj.byorig(orig)
        o.say(channel, txt)
