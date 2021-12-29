# This file is placed in the Public Domain.


"object default"


from obj import Object


class Default(Object):

    def __getattr__(self, k):
        if k in self:
            return self[k]
        return ""
