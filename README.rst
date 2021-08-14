README
######

Welcome to BOTLIB,

BOTLIB is a pure python3 IRC chat bot library that can be used to program
bots.

BOTLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

installation is through pypi::

 $ sudo pip3 install botlib 

default channel/server is #bot on localhost.

CONFIG
======

you can configure the bot with the cfg command, it edits files on disk::

 $ bot cfg server=botd.io channel=\#botd nick=botje

USERS
=====

if the users option is set in the irc config then users need to be added 
before they can give commands::

 $ bot cfg users=true 

use the met command to introduce a user::

 $ bot met ~bart@botd.io
 ok

COMMANDS
========

modules are not loaded from a directory but included in the code itself, so
if you want to program you need to clone the repositry from github::

 $ git clone ssh://git@github.com/bthate/botlib

or download a tar from pypi::

 $ https://pypi.org/project/botlib/#files

open bot/hlo.py (new file) and add the following code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

and add the hlo module to bot/all.py::

   import bot.hlo


the hlo command in now available::

 <bart> !hlo
 hello root@console


PROGRAMMING
===========

the bot package provides a library you can use to program objects 
under python3. It provides a basic Object, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with a little database module, it uses read-only files to
improve persistence and a type in filename for reconstruction.

basic usage is this::

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the bot.obj module has the basic methods like load/save to disk providing bare
persistence::

 >>> wd = "data"
 >>> from bot.obj import Object
 >>> o = Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'bot.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

DEBUG
=====

you can try you force a reinstall of the botd package if it doesn't work::

 $ pip3 install botlib --upgrade --force-reinstall

CONTACT
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
