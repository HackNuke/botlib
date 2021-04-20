# This file is placed in the Public Domain.

from .obj import Object, cfg
from .nms import Names
from .prs import parseargs
from .utl import direct, spl
from .zzz import os, sys

class Loader(Object):

    table = Object()

    @staticmethod
    def boot(wd=None):
        if len(sys.argv) >= 1:
            parseargs(cfg, " ".join(sys.argv[1:]))
            cfg.update(cfg.sets)
        cfg.name = sys.argv[0].split(os.sep)[-1]
        cfg.wd = wd or cfg.wd or os.path.expanduser("~/.%s" % cfg.name)

    def load(self, mnn):
        if mnn in Loader.table:
            return self.table[mnn]
        Loader.table[mnn] = direct(mnn)
        return Loader.table[mnn]

    def init(self, mns):
        for mn in spl(mns):
            m = Names.getinit(mn)
            if not m:
                continue
            mod = self.load(m)
            if mod and "init" in dir(mod):
                mod.init(self)
