# This file is placed in the Public Domain.


import base64


def pwd(event):
    if len(event.prs.args) != 2:
        event.reply("pwd <nick> <password>")
        return
    m = "\x00%s\x00%s" % (event.prs.args[0], event.prs.args[1])
    mb = m.encode("ascii")
    bb = base64.b64encode(mb)
    bm = bb.decode("ascii")
    event.reply(bm)
