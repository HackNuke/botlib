.. _programming:

programming
###########

**BOTLIB** is programmable, to program the bot you have to have the code
available as employing your own code requires that you install your own bot as
the system bot. This is to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runnable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are avoided, the bot
scans modules from sys.path (for now).

**BOTLIB** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more change. Files
paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object. Only include your own written code
**should** be the path to "secure".

code
----

you can fetch the source code (or clone/fork) from git repository.

 ``git clone https://github.com/bthate/botlib``

or download the tar from https://pypi.org/project/botlib/#files

commands
--------

cd into the extracted directory and add your module to the bot package.

 ``joe bot/hlo.py``

add your command code to the file::

  def hlo(event):
     event.reply("hello!")

then add bot/hlo.py to the bot/all.py module and let it scan the module::

  import bot.hlo as hlo
  Table.addmod(hlo)

install the bot on the system and restart bot.
 
 | ``python3 setup.py install``
 | ``systemctl restart botd``

the hlo command is now available to users.
