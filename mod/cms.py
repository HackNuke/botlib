# This is file is placed in Public Domain.

from obj import Names

def register():
    Names.add(cmd)

def cmd(event):
    event.reply(",".join(sorted(Names.modules)))