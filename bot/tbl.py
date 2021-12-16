# This file is placed in the Public Domain.


import inspect


from .obj import Object, get
from .utl import spl


def __dir__():
    return ("Table", "getcls", "getmod", "getobj")


class Table(Object):

    classes = Object()
    modules = Object()
    modnames = Object()
    names = Object()

    @staticmethod
    def add(func):
        n = func.__name__
        Table.modnames[n] = func.__module__

    @staticmethod
    def get(mn):
        return get(Table.modules, mn, None)

    @staticmethod
    def addcls(clz):
        Table.classes[clz.__name__.lower()] = clz
        name = clz.__name__.lower()
        if name not in Table.names:
            Table.names[name] = []
        clzname = "%s.%s" % (clz.__module__, clz.__name__)
        if clzname not in Table.names[name]:
            Table.names[name].append(clzname)

    @staticmethod
    def addmod(mod):
        if mod not in Table.modules:
            Table.modules[mod.__name__.lower()] = mod

    @staticmethod
    def introspect(mod):
        for k, o in inspect.getmembers(mod, inspect.isfunction):
            if k not in Table.modnames:
                if o.__code__.co_argcount == 1:
                    if "event" in o.__code__.co_varnames:
                        Table.add(o)
        for k, o in inspect.getmembers(mod, inspect.isclass):
            if k not in Table.classes and issubclass(o, Object):
                Table.addcls(o)

    @staticmethod
    def scan(pn, ml, init=True, threaded=False):
        for mn in spl(ml):
            mn = "%s.%s" % (pn, mn)
            mod = Table.get(mn)
            Table.introspect(mod)
            if init:
                i = getattr(mod, "init", None)
                if i:
                    if threaded:
                        launch(i)
                    else:
                        i()

def getcls(mn, on):
    mod = Table.classes.get(mn, None)
    if mod:
        return getattr(mod, on, None)


def getmod(mn, on):
    return get(Table.modules, mn, None)


def getobj(mn, on):
    mod = Table.modules.get(mn, None)
    if mod:
        return getattr(mod, on, None)
