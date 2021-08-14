# This is file is placed in Public Domain.

"cms shows list of commands"

from bot.krn import kernel

def cmd(event):
    k = kernel()
    event.reply(",".join(sorted(k.cmds)))
