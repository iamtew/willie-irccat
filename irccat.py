import willie
import socket
import thread

HOST = '0.0.0.0'
PORT = 5234

def setup(bot):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    # sock.setblocking(0)


def shutdown(bot):
    sock.close()

@willie.module.commands('netpipe')
def netpipe(bot, trigger):
    def pipe():
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            print 'From: ' + addr[0] + ':' + str(addr[1])
            print ' Msg: ' + data
            bot.say(data)
            if not data:
                break
            conn.close()

    thread.start_new_thread(pipe, ())
