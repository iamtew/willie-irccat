# coding=utf8

import os
import willie
import socket

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
    # sock.setblocking(0)


def shutdown(bot):
    """
    Close socket at bot shutdown
    """
    sock.close()


@willie.module.event('001', '251')
@willie.module.rule('.*')
def netpipe(bot, trigger):
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)

        pipelog = open(os.path.join(bot.config.logdir, 'netpipe.log'), 'a')
        pipelog.write('message from ' + addr[0] + ': ' + data)

        chan, msg = data.split(' ', 1)
        if chan in bot.config.core.channels:
            bot.msg(chan, msg)

        if not data:
            break

        conn.close()
        pipelog.close()
