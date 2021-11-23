**24/7 channel daemon**

B O T L I B
###########

name
====

**BOTLIB** - OS level integration of bot technology.

synopsis
========

| ``bot <cmd> [key=value] [key==value]``
| ``bot cfg server=<server> channel=<channel> nick=<nick>`` 
| ``bot -cv mod=irc,rss``

| ``(*) default channel/server is #bot on localhost``

description
===========

A solid, non hackable bot, that runs under systemd as a 24/7 background
service and starts the bot after reboot, intended to be programmable in a
static, only code, no popen, no imports and no reading modules from a
directory, way that **should** make it suitable for embedding.

install
=======

``pip3 install botlib``

configuration
=============

configuration is done by calling the bot as a cli, bot <cmd> allows you to
run bot commands on a shell. use the cfg command to edit configuration on
disk, the botd background daemon uses the botctl program.

sasl
----

| ``bot pwd <nickservnick> <nickservpass>``
| ``bot cfg password=<outputfrompwd>``

users
-----

| ``bot cfg users=True``
| ``bot met <userhost>``

rss
---

| ``bot rss <url>``

24/7
----

| ``cp /usr/local/share/botd/botd.service /etc/systemd/system``
| ``botctl cfg server=<server> channel=<channel> nick=<nick>`` 
| ``systemctl enable botd --now``
