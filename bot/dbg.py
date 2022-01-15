# This file is placed in the Public Domain.


from bot.tbl import Cmd


def rse(event):
    raise Exception("debug!")


Cmd.add(rse)
