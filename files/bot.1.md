% BOT(1) BOT version 130
% Bart Thate <bthate67@gmail.com>
% Aug 2021

# NAME
BOT - python3 irc bot

# SYNOPSIS

| bot \<cmd>\ [options] [key=value] [key==value]

| -b	\# bork mode
| -c	\# start client
| -d	\# start daemon
| -v	\# use verbose
 
# CONFIGURATION

| bot cfg server=localhost channel=\#bot nick=bot
| bot m=irc,rss

| bot pwd \<nick\> \<password\>
| bot cfg password=\<outputofpwd\>

| bot cfg users=true 
| bot met \<userhost\>

| bot rss \<url\>

# DESCRIPTION

BOT is a pure python3 IRC chat bot that can run as a background daemon for
24/7 a day presence in a IRC channel, it can be used to display RSS
feeds, act as a UDP to IRC relay and you can program your own commands for it.

BOT an attempt to achieve OS level integration of bot technology directly
into the operating system. A solid, non hackable bot version, that can offer
"display in your irc channel" functionality to the unix programmer. BOTLIB
runs on both BSD and Linux, is placed in the Public Domain, and, one day,
will be the thing you cannot do without ;]

# ENVIRONMENT

the bot package provides a library you can use to program objects 
under python3. It provides a basic Object, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with a little database module, it uses read-only files to
improve persistence and a type in filename for reconstruction::

    def getmain(name):
         return getattr(sys.modules["__main__"], name, None)
    
    clt = getmain("clt")
    k = getmain("k")
    tbl = getmain("tbl")

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

basic usage is this.

    from bot.obj import Object
    o = Object()
    o.key = "value"
    o.key
    'value'

load/save from/to disk.

    from bot.obj import Object, load, save
    o = Object()
    o.key = "value"
    p = save(o)
    oo = Object()
    load(oo, p)
    oo.key
    'value'

great for giving objects peristence by having their state stored in files.

# COPYRIGHT

**BOT** is placed in the Public Domain, no COPYRIGHT, no LICENSE.

