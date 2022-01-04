# This file is placed in the Public Domain.


from .obj import Object, values
from .fnc import index

class Bus(Object):

    objs = Object()

    @staticmethod
    def add(o):
        print(repr(o))
        print(values(Bus.objs))
        if o not in values(Bus.objs):
            print("adding %s" % repr(o))
            index(Bus.objs, o)

    @staticmethod
    def announce(txt):
        for o in values(Bus.objs):
            o.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in values(Bus.objs):
            if repr(o) == orig:
                return o
        
    @staticmethod
    def say(orig, channel, txt):
        o = Bus.byorig(orig)
        if o:
            o.say(channel, txt)
