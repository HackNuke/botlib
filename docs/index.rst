BOTLIB
######

**BOTLIB** is an attempt to achieve OS level integration of bot technology
directly into the operating system. A solid, non hackable bot, that runs
under rc.d as a 24/7 background service that starts the bot after reboot.
**BOTLIB** is intended to be programmable in a static, only code, no popen, no
imports and no reading modules from a directory, way that **should** make
it suitable for embedding.

**BOTLIB** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more change. Files
paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object. Only include your own written code
**should** be the path to "secure".

INSTALL
=======

installation is through pypi or run python3 from the tarball (run
install_data as well).

 pip3 install botlib


CONFIGURATION
=============

configuration is done by calling the bot as a cli, bot <cmd> allows you to
run bot commands on a shell, configuration uses the cfg command to edit 
configuration on disk. 

irc
---

IRC configuration is done with the use of the botctl program, the cfg
command configures the IRC bot.

 bot cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

(*) default channel/server is #botd on localhost

sasl
----

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this.

 bot pwd \<nickservnick\> \<nickservpass\>

after creating you sasl password add it to you configuration.

 bot cfg password=\<outputfrompwd\>

users
-----

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

 | bot cfg users=True
 | bot met \<userhost\>

rss
---

if you want rss feeds in your channel install feedparser. to add an url to
the bot and the feed fetcher will poll it every 5 minutes.

 bot rss \<url\>

24/7
----

if you want to bot restarted after reboot, enable the systemd service.

 | cp /usr/local/share/botd/botd.service /etc/systemd/system  
 | systemctl enable botd --now

the botd program uses botc as it's cli for configuration.

 | botc cfg
 | cc=! channel=#botd nick=botd port=6667 server=localhost sleep=30


PROGRAMMING
===========

**BOTLIB** is programmable, to program the bot you have to have the code
available as employing your own code requires that you install your own bot as
the system bot. This is to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runnable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are avoided, the bot
scans modules from sys.path.

you can fetch the source code (or clone/fork) from git repository.

 git clone https://github.com/bthate/botlib

or you can get the code as a tar on pypi, you can download from https://pypi.org/project/botlib/#files

commands
--------

untar the tarball, cd into the extracted directory and add your module to the
bot package.

 joe bot/hlo.py

add your command code to the file::

 def hlo(event):
     event.reply("hello!")

then add bot/hlo.py to the bot/all.py module and let it scan the module::

 import bot.hlo as hlo
 Table.addmod(hlo)

install the bot on the system.

 python3 setup.py install

restart botd service.

 systemctl restart botd

the hlo command is now available to users.


.. toctree::
    :hidden:
    :glob:

    *
