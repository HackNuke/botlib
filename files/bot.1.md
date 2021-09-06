% BOT(1) BOTLIB version 130
% Bart Thate 
% Sep 2021

# NAME

BOT - pure python3 irc bot

# SYNOPSIS

| bot \<cmd>\ [options] [key=value] [key==value]
| bot mod=irc,rss

# DESCRIPTION

**BOTLIB** is a library to program bots and **BOT** is it's demo program.

**BOT** is a IRC bot that can run in a IRC channel. You can use it to
display RSS feeds, act as a UDP to IRC gateway, program your own commands
for it and have it log objects on disk to search them. 

 
# CONFIGURATION

| bot cfg server=localhost channel=\#bot nick=bot
| bot mod=irc,rss

| bot pwd \<nick\> \<password\>
| bot cfg password=\<outputofpwd\>

| bot cfg users=true 
| bot met \<userhost\>

| bot rss \<url\>

# OPTIONS

| -b	\# bork mode
| -c	\# start client
| -d	\# daemon mode
| -v	\# use verbose
