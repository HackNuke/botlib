NAME
====

**BOTLIB** - python3 bot library - https://pypi.org/project/botlib

SYNOPSIS
========

bot \<cmd\> \|options\] \[key=value\] \[key==value\]

DESCRIPTION
===========

**BOTLIB** is a library to program bots and **BOT** is it's demo program.

the bot package provides a library you can use to program objects 
under python3, an Object class, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with database functions and uses read-only files to
improve persistence and a type in filename for reconstruction.

**BOT** is a IRC bot that can run as a  background daemon for 24/7 a day
presence in a IRC channel. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it and have it log
objects on disk to search them. 

INSTALL
=======

| sudo pip3 install botlib

CONFIGURATION
=============

| bot cfg server=\<server\> channel=<channel> nick=\<nick\>

| bot cfg users=True
| bot met \<userhost\>

| bot pwd \<nickservnick\> \<nickservpass\>
| bot cfg password=\<outputfrompwd\>

| bot rss \<url\>

| \* default channel/server is #bot on localhost

FILES
=====

| bin/bot
| man/man1/bot.1.gz

COPYRIGHT
=========

**BOTLIB** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

| Bart Thate <bthate67@gmail.com>
