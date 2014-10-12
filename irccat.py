# coding=utf8
"""
irccat.py - Network socket listener
Copyright (c) 2014 Mikael Sörlin <iamtew@asylunatic.se>
Licensed under the MIT License.

https://github.com/iamtew/willie-irccat
"""

import os
import re
import socket
from datetime import datetime
from willie.config import ConfigurationError
from willie import module


def irccat_config(bot):
    if not bot.config.has_option('irccat', 'address') or \
       not bot.config.has_option('irccat', 'port'):
        return False
    else:
        return [bot.config.irccat.address, bot.config.irccat.port]


def configure(config):
    """
    | [irccat] | example | purpose        |
    | -------- | ------- | -------------- |
    | address  | 0.0.0.0 | Listen address |
    | port     | 5234    | Listen port    |
    """
    if config.option('Listening address and port for irccat', False):
        config.interactive_add('irccat', 'address', 'Listen address', '0.0.0.0')
        config.interactive_add('irccat', 'port', 'Listen port', '5234')


def setup(bot):
    if not irccat_config(bot):
        raise ConfigurationError('irccat module not configured')


@module.event('001')
@module.rule('.*')
def netpipe(bot, trigger):
    """
    Open our listening socket upon successfull server connection when the bot
    receives RPL_WELCOME (001)
    """
    netcfg = irccat_config(bot)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((netcfg[0], int(netcfg[1])))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)

        if not data.rstrip('\r\n'):
            break

        logfile = open(os.path.join(bot.config.logdir, 'irccat.log'), 'a')
        logfile.write(str(datetime.now()) + ' msg ' + addr[0] + ': ' + data)

        # First part of the message should be channel/user
        rcpt, msg = data.split(' ', 1)
        if ',' in rcpt:
            rcpts = rcpt.split(',')
            for target in rcpts:
                if target in bot.config.core.channels:
                    bot.msg(target, msg)
                elif re.search('^@', target):
                    bot.msg(re.sub('^@', '', target), msg)
        else:
            if re.search('^@', rcpt):
                bot.msg(re.sub('^@', '', rcpt), msg)
            elif re.search('^#', rcpt):
                bot.msg(rcpt, msg)
            else:
                chanlist = bot.config.channels.split(',', 1)
                bot.msg(chanlist[0], data)

        conn.close()
        logfile.close()

    sock.close()
