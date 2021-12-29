# This file is placed in the Public Domain.


"object parse"


from obj import Object
from odf import Default


class Parsed(Default):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

    def args(self):
        return " ".join(self.txt.split()[1:])

    def cmd(self):
        if self.txt:
            return self.txt.split()[0].lower()

    def gets(self):
        return Object([(x.split("==")[0], x.split("==")[-1]) for x in self.txt.split() if "==" in x])

    def opts(self):
        return Object([(x[1:], True) for x in self.txt.split() if x.startswith("-")])

    def sets(self):
        return Object([(x.split("=")[0], x.split("=")[-1]) for x in self.txt.split() if "=" in x])


    def rest(self):
        return " ".join([x for x in self.txt.split()[1:]
                   if "=" not in x and "-" not in x])
