# This file is placed in the Public Domain.


from . import Object, values


class Bus(Object):

    objs = []

    @staticmethod
    def add(o):
        if o not in Bus.objs:
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
