# This file is placed in the Public Domain.


"command"


from .fnc import register
from .obj import Object, get


class Cmd(Object):

    cmds = Object()

    @staticmethod
    def add(cmd):
        register(Cmd.cmds, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        return get(Cmd.cmds, cmd)
