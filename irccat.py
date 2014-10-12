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
    """Return our configuration or False"""
    if not bot.config.has_option('irccat', 'address') or \
       not bot.config.has_option('irccat', 'port'):
        return False
    else:
        return [bot.config.irccat.address, bot.config.irccat.port]


def irccat_logger(bot, src, body, level=False):
    """
    Write messages to our log with timestamp and source IP.
    Also write to debug log if we set a level
    """
    message = str(datetime.now()) + ': From: ' + src + ':' + body
    logfile = open(os.path.join(bot.config.logdir, 'irccat.log'), 'a')
    logfile.write(message)
    logfile.close()

    if level is not False:
        bot.debug('irccat', message, level)


def irccat_targets(bot, targets):
    """
    Go through our potential targets and place them in an array so we can
    easily loop through them when sending messages.
    """
    result = []
    if ',' in targets:
        for s in targets.split(','):
            if re.search('^@', s):
                result.append(re.sub('^@', '', s))

            elif re.search('^#', s) and s in bot.config.core.channels:
                result.append(s)
    else:
        if re.search('^@', targets):
            result.append(re.sub('^@', '', targets))

        elif re.search('^#', targets):
            result.append(targets)

    return result


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

        if not len(data.split()) >= 2:
            errmsg = 'Too short message received'
            irccat_logger(bot, addr[0], errmsg + ': ' + data, 'warning')
            conn.close()
            continue

        irccat_logger(bot, addr[0], 'Received: ' + data)

        target, message = data.split(' ', 1)
        for chat in irccat_targets(bot, target):
            bot.msg(chat, message)

        conn.close()

    sock.close()
