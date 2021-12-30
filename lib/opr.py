# This file is placed in the Public Domain.


"object parse"


from obj import Object
from odf import Default


class Parsed(Default):

    def __init__(self, txt):
        super().__init__()
        self.otxt = txt
        self._txt = txt

    @property
    def args(self):
        return self._txt.split()[1:]

    @property
    def cmd(self):
        if self.txt:
            return self._txt.split()[0].lower()

    @property
    def gets(self, keyz=None):
        return Object([(x.split("==")[0], x.split("==")[-1]) for x in self._txt.split() if "==" in x])

    @property
    def opts(self):
        return Object([(x[1:], True) for x in self._txt.split() if x.startswith("-")])

    @property
    def sets(self):
        return Object([(x.split("=")[0], x.split("=")[-1]) for x in self._txt.split() if "=" in x])

    @property
    def rest(self):
        return " ".join([x for x in self._txt.split()[1:]
                   if "=" not in x and "-" not in x])

    @property
    def txt(self):
        return self._txt.split(":", 2)[-1]
