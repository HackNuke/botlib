# This file is placed in the Public Domain.

"errors"

class Error(Exception):

    "basic error class."

class Restart(Error):

    "restarts the handler."


class Stop(Error):

    "stops handler loop."


class Break(Error):

    "breaks the handler loop."


class NotImplemented(Error):

    "method is not implemented in inherited class."



class NoBot(Error):

    "no orig matching bot is found in fleet."


class NoFile(Error):

    "file was not found."


class NoJSON(Error):

    "no json compatible data was read."


class NoModule(Error):

    "module was not imporable"


class NoType(Error):

    "type is not supported."
