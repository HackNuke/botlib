BOTLIB
######

**BOTLIB** is an attempt to achieve OS level integration of bot technology
directly into the operating system. A solid, non hackable bot, that runs
under systemd and rc.d as a 24/7 background service that starts the
bot after reboot, stores it's data as JSON files on disk, every object is
timestamped, readonly of which the latest is served to the user layer. This
bot is intended to be programmable in a static, only code, no popen, no
imports and no reading modules from a directory, way that **should** make
it suitable for embedding - :ref:`source`, :ref:`programming`

configuration
=============

configuration is done by calling the bot as a cli, bot <cmd> allows you to
run bot commands on a shell, configuration uses the cfg command to edit 
configuration on disk. 

irc
---

IRC configuration is done with the use of the botctl program, the cfg
command configures the IRC bot.

::

 bot cfg server=<server> channel=<channel> nick=<nick> 

default channel/server is #botd on localhost

sasl
----

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this

::

 bot pwd <nickservnick> <nickservpass>

after creating you sasl password add it to you configuration.

::

 bot cfg password=<outputfrompwd>

users
-----

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

::

 bot cfg users=True
 bot met <userhost>

rss
---

if you want rss feeds in your channel install feedparser.

::

 sudo apt install python3-feedparser

add a url to the bot and the feed fetcher will poll it every 5 minutes.

::

 bot rss <url>

24/7
----

if you want to bot to restart after reboot, enable the botd rc.d script:

::

 $ doas rcctl enable botd
 $ doas rcctl start botd

the botd program uses botc as it's cli for configuration:

::

  $ doas botc cfg


, botctl is
a systemd wrapper around it. depending on rc.d or systemd choose one of
those.


.. toctree::
    :hidden:
    :glob:

    *
