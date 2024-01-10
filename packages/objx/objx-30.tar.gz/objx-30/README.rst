NAME

::

    OBJX - objects library.


SYNOPSIS

::

    >>> from objx import Object
    >>> o = Object()
    >>> o.a = "b"
    >>> write(o, "test")
    >>> oo = Object()
    >>> read(oo, "test")
    >>> oo
    {"a": "b"}  



DESCRIPTION

::

    OBJX provides an objx namespace that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OBJX is a python3 library implementing the 'objx' package. It
    provides all the tools to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OBJX provides a demo bot, if you also it can connect to IRC, fetch and
    display RSS feeds, take todo notes, keep a shopping list
    and log text. You can also copy/paste the service file and run
    it under systemd for 24/7 presence in a IRC channel.

    OBJX is Public Domain.


INSTALL

::

    $ pipx install objx


USAGE


synopsis

::

    objx <cmd> [key=val] 
    objx <cmd> [key==val]
    objx [-c] [-v] [-d]


without any argument the program does nothing

::

    $ objx
    $

see list of commands

::
    $ objx cmd
    cmd,err,mod,req,thr,ver

list of modules

::

    $ objx mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr

use mod=<name1,name2> to load additional modules

::

    $ objx cfg mod=irc

start a console


::

    $ objx -c mod=irc,rss
    >

use -v for verbose


::

    $ objx -cv mod=irc
    OBJX started CV started Sat Dec 2 17:53:24 2023
    >

start daemon

::

    $ objd
    $ 


CONFIGURATION

irc

::

    $ objx cfg server=<server>
    $ objx cfg channel=<channel>
    $ objx cfg nick=<nick>

sasl

::

    $ objx pwd <nsvnick> <nspass>
    $ objx cfg password=<frompwd>

rss

::

    $ objx rss <url>
    $ objx dpl <url> <item1,item2>
    $ objx rem <url>
    $ objx nme <url< <name>


COMMANDS

::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    thr - show the running threads


SYSTEMD

save the following it in /etc/systems/system/objx.service and
replace "<user>" with the user running pipx

::

    [Unit]
    Description=objects daemon
    Requires=network.target
    After=network.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objx
    ExecStart=/home/<user>/.local/pipx/venvs/objx/bin/objd
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


then run this

::

    $ mkdir ~/.objx
    $ sudo systemctl enable objx --now

default channel/server is #objx on localhost


FILES

::

    ~/.objx
    ~/.local/bin/objx
    ~/.local/bin/objd
    ~/.local/pipx/venvs/objx/


AUTHOR

::

    Bart Thate <libbotx@gmail.com>


COPYRIGHT

::

    OBJX is Public Domain.
