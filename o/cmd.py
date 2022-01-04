# This file is placed in the Public Domain.


from .obj import Object, get


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
        e.ready()

    @staticmethod
    def get(cmd):
        return get(Cmd.cmds, cmd)

