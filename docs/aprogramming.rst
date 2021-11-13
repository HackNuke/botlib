PROGRAMMING
###########

**BOTD** is an attempt to achieve OS level integration of bot technology
directly into the operating system. A solid, non hackable bot, that runs
under systemd and rc.d as a 24/7 background service that starts the
bot after reboot, stores it's data as JSON files on disk, every object is
timestamped, readonly of which the latest is served to the user layer. This
bot is intended to be programmable in a static, only code, no popen, no
imports and no reading modules from a directory, way that makes it suitable
for embedding.

description
===========

For programming the bot you have to have the code available as employing
your own code requires that you install your own bot as the system bot.

This is to not have a directory to read modules from to add commands to the
bot but include the own programmed modules directly into the python code.

This way only trusted code (your own written code) is included and runnable.
Reading random code from a directory is what gets avoided.

As experience tells os.popen and __import__, importlib are avoided, the bot
scans modules from sys.path. Maybe sys.path security issues need to be
adressed again. This also avoids running other then own written code.

Data is stored on disk where objects are time versioned and the last version
saved on disk is served to the user layer. Files are JSON dumps that are
read-only so thus should provide (disk) persistence more change. Files paths
carry the type in the path name what makes reconstruction from filename
easier then reading type from the object. 

Only include your own written code should be the path to "secure".

commands
========

fetch the code from https://pypi.org/project/botd/#files

untar the tarball, cd into the bot directory and add your module to the bot
packages:

 > joe bot/hlo.py

add your command code to the file:

 >>> def hlo(event):
 >>>     event.reply("hello!")

then add bot/hlo.py to the bot/all.py module and let it scan the module.

 >>> import bot.hlo as hlo
 >>> Table.addmod(hlo)

create wheel again:

 > python3 setup.py bdist_wheel

install wheel:

 > sudo pip3 install dist/botd-67-py3-none-any.whl

restart botd service:

 > sudo systemctl restart botd

the hlo command is now available to users.

copyright
=========

**BOTD** is placed in the Public Domain, no Copyright, no LICENSE.

author
======

Bart Thate
