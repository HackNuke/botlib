B O T L I B
###########

**BOTLIB** is an attempt to achieve OS level integration of bot technology
directly into the operating system. A solid, non hackable bot, that runs
under systemd as a 24/7 background service that starts the bot after reboot.

**BOTLIB** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more change. Files
paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object. Only include your own written code
**should** be the path to "secure".

**BOTLIB** is intended to be programmable in a static, only code, no popen, no
imports and no reading modules from a directory, way that **should** make
it suitable for embedding.

install
=======

 pip3 install botlib


configuration
=============

configuration is done by calling the bot as a cli, bot <cmd> allows you to
run bot commands on a shell, configuration uses the cfg command to edit 
configuration on disk. 

irc
---

 bot cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

 (*) default channel/server is #bot on localhost

sasl
----

 | bot pwd \<nickservnick\> \<nickservpass\>
 | bot cfg password=\<outputfrompwd\>

users
-----

 | bot cfg users=True
 | bot met \<userhost\>

rss
---

 bot rss \<url\>

24/7
----

if you want to bot restarted after reboot, enable the systemd service.

 | cp /usr/local/share/botd/botd.service /etc/systemd/system  
 | systemctl enable botd --now

the botd program uses botctl as it's cli for configuration.

 | botctl cfg
 | cc=! channel=#botd nick=botd port=6667 server=localhost sleep=30

 (*) default channel/server is #botd on localhost

programming
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
