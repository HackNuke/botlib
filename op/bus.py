# This file is placed in the Public Domain.


"list of listeners"


from .obj import Object


class Bus(Object):

    objs = []

    @staticmethod
    def add(o):
        if repr(o) not in [repr(o) in Bus.objs]:
            Bus.objs.append(o)

    @staticmethod
    def announce(txt):
        for o in Bus.objs:
            o.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    @staticmethod
    def say(orig, channel, txt):
        o = Bus.byorig(orig)
        if o:
            o.say(channel, txt)