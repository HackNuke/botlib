% BOT(1) BOT(1)
% Bart Thate
% Aug 2021

# NAME
BOT - python3 irc bot

# SYNOPSIS
| bot \<cmd>\ 
| bot cfg server=irc.freenode.net channel=\\#bot
| bot m=irc,rss

# DESCRIPTION
BOT an attempt to achieve OS level integration of bot technology directly
into the operating system. A solid, non hackable bot version, that can offer
"display in your irc channel" functionality to the unix programmer. BOTLIB
runs on both BSD and Linux, is placed in the Public Domain, and, one day,
will be the thing you cannot do without ;]

# EXAMPLES

| $ bot
| $ 

| $ bot cmd
| cfg,cmd,dlt,ech,exc,flt,fnd,krn,met,sve,thr,upt,ver

| $ bot cfg
| cc=@ channel=#botd nick=botd port=6667 server=localhost

| bot krn
| $ cmd=krn name=bot txt=krn users=True version=1 wd=/home/bart/.bot

| $ bot thr
| CLI.handler 0s | CLI.input 0s

| $ bot m=bot.irc,bot.rss
| >

# SEE ALSO
| botd
| botctl
| ~/.bot
| ./mod

# COPYRIGHT
BOTLIB is placed in the Public Domain, no COPYRIGHT, no LICENSE.
