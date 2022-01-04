# This file is placed in the Public Domain.

"object runtime"


from .dft import Default


class Cfg(Default):

    console = False
    debug = False
    verbose = False
    wd = ""
