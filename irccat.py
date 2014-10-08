# coding=utf8

import os
import re
import willie
import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5234

def setup(bot):
    """
    Open listening socket on bot startup
    """
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)


def shutdown(bot):
    """
    Close socket at bot shutdown
    """
    sock.close()


@willie.module.event('001')
@willie.module.rule('.*')
def netpipe(bot, trigger):
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        logfile = open(os.path.join(bot.config.logdir, 'irccat.log'), 'a')
        logfile.write(str(datetime.now()) + ' message from ' + addr[0] + ': ' + data)

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


        if not data:
            break

        conn.close()
        logfile.close()
