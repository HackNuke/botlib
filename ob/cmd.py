# This file is placed in the Public Domain.


from . import Object, get
from .fnc import register

class Cmd(Object):

    cmds = Object()

    @staticmethod
    def add(cmd):
        register(Cmd.cmds, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        return get(Cmd.cmds, cmd)
