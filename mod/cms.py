# This is file is placed in Public Domain.

from bl.krn import kernel

def cmd(event):
    k = kernel()
    event.reply(",".join(sorted(k.cmds)))
