# This is file is placed in Public Domain.

from bot.krn import kernel

def cmd(event):
    k = kernel()
    event.reply(",".join(sorted(k.cmds)))
