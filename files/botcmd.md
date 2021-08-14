% BOTCMD(1) BOTCMD(1)
% Bart Thate
% Aug 2021

# NAME
BOT - client version of botd

# SYNOPSIS
| botcmd \<cmd>\ 
| botcmd cfg server=irc.freenode.net channel=\\#botd

# DESCRIPTION
BOTCMD is the CLI version of BOTD.

# EXAMPLES

| $ botcmd
| $ 

| $ botcmd cmd
| cfg,cmd,dlt,ech,exc,flt,fnd,krn,met,sve,thr,upt,ver

| $ botcmd cfg
| cc=@ channel=#botd nick=botd port=6667 server=localhost

| botcmd krn
| $ cmd=krn name=bot txt=krn users=True version=1 wd=/home/bart/.bot

| $ botcmd thr
| CLI.handler 0s | CLI.input 0s

# SEE ALSO
| botd
| botctl
| /var/lib/botd

# COPYRIGHT
BOTCMD is placed in the Public Domain.
