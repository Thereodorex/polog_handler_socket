import os
from handler.client.socket_sender import Socket_Sender

from polog import config
from polog import flog


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

config.add_handlers(Socket_Sender(HOST, PORT))

class Kek:

    def __init__(self):
        self.kek = 1

@flog
def logged_func(arg):
    return arg

def client_test():
    for i in range(10):
        pid = os.fork()
        if not pid:
            break
    logged_func('First test string')